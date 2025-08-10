# BitkiAI/utils.py

from celery import chain
from .tasks import upload_image, preprocess_image, predict_image, save_result
from .models import WorkflowStep, Workflow

def run_workflow(file_bytes: bytes, filename: str, workflow_id: int) -> str:
    workflow = Workflow.objects.get(pk=workflow_id)
    base     = workflow.steps.count()

    upload_step     = WorkflowStep.objects.create(
        workflow=workflow, name='Görsel Yükleme',   task_name='upload_image',     order=base+1
    )
    preprocess_step = WorkflowStep.objects.create(
        workflow=workflow, name='Ön İşleme',        task_name='preprocess_image', order=base+2
    )
    predict_step    = WorkflowStep.objects.create(
        workflow=workflow, name='Tahmin',           task_name='predict_image',    order=base+3
    )
    save_step       = WorkflowStep.objects.create(
        workflow=workflow, name='Sonuç Kaydetme',   task_name='save_result',      order=base+4
    )

    task_chain = chain(
        upload_image.s(
            file_bytes, filename,
            upload_step.id,
            preprocess_step.id,
            predict_step.id,
            save_step.id
        ),
        preprocess_image.s(),
        predict_image.s(),
        save_result.s()
    )
    result = task_chain.apply_async()

    workflow.status = 'started'
    workflow.save()

    return result.id
