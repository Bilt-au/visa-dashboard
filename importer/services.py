import pandas as pd
from django.db import transaction
from data.models import VisaType, Occupation, MonthYear, VisaData


class ExcelImportService:
    def __init__(self):
        self.required_columns = [
            'As At Month', 'Visa Type', 'Occupation',
            'EOI Status', 'Points', 'Count EOIs'
        ]

    def validate_file(self, file_path):
        try:
            df = pd.read_excel(file_path)
            missing_columns = [col for col in self.required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            return True
        except Exception as e:
            raise ValueError(f"Invalid Excel file: {str(e)}")

    def process_excel_file(self, file_path):
        self.validate_file(file_path)

        # Read the entire Excel file
        df = pd.read_excel(file_path)

        results = {
            'total_rows': len(df),
            'processed': 0,
            'errors': []
        }

        # Process in chunks to avoid memory issues
        chunk_size = 1000

        # Pre-fetch existing objects to reduce DB queries
        existing_visa_types = {vt.name: vt for vt in VisaType.objects.all()}
        existing_occupations = {oc.name: oc for oc in Occupation.objects.all()}
        existing_month_years = {my.name: my for my in MonthYear.objects.all()}

        for start_idx in range(0, len(df), chunk_size):
            end_idx = min(start_idx + chunk_size, len(df))
            chunk_df = df.iloc[start_idx:end_idx]

            self._process_chunk(chunk_df, results, existing_visa_types, existing_occupations, existing_month_years)

        return results

    def _process_chunk(self, chunk_df, results, existing_visa_types, existing_occupations, existing_month_years):
        visa_data_objects = []

        for index, row in chunk_df.iterrows():
            try:
                # Process row and create object (don't save yet)
                visa_data = self._prepare_visa_data_object(
                    row, existing_visa_types, existing_occupations, existing_month_years
                )
                visa_data_objects.append(visa_data)
                results['processed'] += 1
            except Exception as e:
                results['errors'].append(f"Row {index + 1}: {str(e)}")

        # Bulk create all objects at once
        if visa_data_objects:
            VisaData.objects.bulk_create(visa_data_objects, ignore_conflicts=True)

    def _process_row(self, row):
        month_year = self._get_or_create_month_year(row['As At Month'])
        visa_type = self._get_or_create_visa_type(row['Visa Type'])
        occupation = self._get_or_create_occupation(row['Occupation'])

        eoi_status = str(row['EOI Status']).upper()
        if eoi_status not in [choice[0] for choice in VisaData.Status.choices]:
            raise ValueError(f"Invalid EOI Status: {eoi_status}")

        points = self._process_points_or_count(row['Points'])
        count_eois = self._process_points_or_count(row['Count EOIs'])

        VisaData.objects.create(
            month_year=month_year,
            visa_type=visa_type,
            occupation=occupation,
            status=eoi_status,
            points=points,
            count=count_eois
        )

    def _get_or_create_month_year(self, month_year_str):
        month_year_str = str(month_year_str).strip()
        month_year, created = MonthYear.objects.get_or_create(
            name=month_year_str
        )
        return month_year

    def _get_or_create_visa_type(self, visa_type_str):
        visa_type_str = str(visa_type_str).strip()
        visa_type, created = VisaType.objects.get_or_create(
            name=visa_type_str
        )
        return visa_type

    def _get_or_create_occupation(self, occupation_str):
        occupation_str = str(occupation_str).strip()
        occupation, created = Occupation.objects.get_or_create(
            name=occupation_str
        )
        return occupation

    def _prepare_visa_data_object(self, row, existing_visa_types, existing_occupations, existing_month_years):
        # Get or create related objects
        month_year_name = str(row['As At Month']).strip()
        if month_year_name not in existing_month_years:
            month_year = MonthYear.objects.create(name=month_year_name)
            existing_month_years[month_year_name] = month_year
        else:
            month_year = existing_month_years[month_year_name]

        visa_type_name = str(row['Visa Type']).strip()
        if visa_type_name not in existing_visa_types:
            visa_type = VisaType.objects.create(name=visa_type_name)
            existing_visa_types[visa_type_name] = visa_type
        else:
            visa_type = existing_visa_types[visa_type_name]

        occupation_name = str(row['Occupation']).strip()
        if occupation_name not in existing_occupations:
            occupation = Occupation.objects.create(name=occupation_name)
            existing_occupations[occupation_name] = occupation
        else:
            occupation = existing_occupations[occupation_name]

        eoi_status = str(row['EOI Status']).upper()
        if eoi_status not in [choice[0] for choice in VisaData.Status.choices]:
            raise ValueError(f"Invalid EOI Status: {eoi_status}")

        points = self._process_points_or_count(row['Points'])
        count_eois = self._process_points_or_count(row['Count EOIs'])

        return VisaData(
            month_year=month_year,
            visa_type=visa_type,
            occupation=occupation,
            status=eoi_status,
            points=points,
            count=count_eois
        )

    def _process_points_or_count(self, value):
        value_str = str(value).strip()
        if value_str == "<20":
            return 0
        try:
            return int(float(value_str))
        except (ValueError, TypeError):
            return 0