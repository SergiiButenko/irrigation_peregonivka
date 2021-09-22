from devices.service_providers.celery import celery_app


@celery_app.task(acks_late=True)
def try_execure_rule(rule_id: str) -> str:
    return f"test task return {rule_id}"