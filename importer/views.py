from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import tempfile
import os
from .services import ExcelImportService


@csrf_exempt
@require_http_methods(["POST"])
def upload_excel(request):
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file provided'}, status=400)

    file = request.FILES['file']

    if not file.name.endswith(('.xlsx', '.xls')):
        return JsonResponse({'error': 'Invalid file format. Please upload an Excel file.'}, status=400)

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name

        service = ExcelImportService()
        results = service.process_excel_file(temp_file_path)

        os.unlink(temp_file_path)

        return JsonResponse({
            'message': 'File processed successfully',
            'results': results
        })

    except ValueError as e:
        if 'temp_file_path' in locals():
            os.unlink(temp_file_path)
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        if 'temp_file_path' in locals():
            os.unlink(temp_file_path)
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)
