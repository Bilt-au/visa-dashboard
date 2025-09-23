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
        df = pd.read_excel(file_path)

        results = {
            'total_rows': len(df),
            'processed': 0,
            'errors': []
        }

        with transaction.atomic():
            for index, row in df.iterrows():
                try:
                    self._process_row(row)
                    results['processed'] += 1
                except Exception as e:
                    results['errors'].append(f"Row {index + 1}: {str(e)}")

        return results

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

    def _process_points_or_count(self, value):
        value_str = str(value).strip()
        if value_str == "<20":
            return 0
        try:
            return int(float(value_str))
        except (ValueError, TypeError):
            return 0