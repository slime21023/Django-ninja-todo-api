from shared.models import Task
from ninja import NinjaAPI, ModelSchema, Schema
from typing import List

api = NinjaAPI()


class TaskSchema(ModelSchema):
    class Config:
        model = Task
        model_fields = ["id", "title", "description", "created_at", "completed"]


class TaskCreateSchema(Schema):
    title: str
    description: str = None


class TaskUpdateSchema(Schema):
    title: str = None
    description: str = None
    completed: bool = None


class Error(Schema):
    message: str


@api.get("/tasks", response=List[TaskSchema])
def list_tasks(request):
    """
    取得所有任務的列表
    """
    todos = Task.objects.all()
    return todos


@api.get("/tasks/{task_id}", response={200: TaskSchema, 404: Error})
def get_task(request, task_id: int):
    """
    取得任務的詳細資訊
    """
    if Task.objects.filter(id=task_id).exists():
        todo = Task.objects.get(id=task_id)
        return todo
    else:
        return 404, {"message": "Task not found"}


@api.post("/tasks", response={201: None})
def create_task(request, payload: TaskCreateSchema):
    """
    建立一個新的任務
    """
    task_value = payload.model_dump()
    Task.objects.create(
        title=task_value.get("title"),
        description=task_value.get("description"),
    )
    return 201, None


@api.put("/tasks/{task_id}", response={204: None})
def update_task(request, task_id: int, payload: TaskUpdateSchema):
    """
    更新一個任務
    """
    task = Task.objects.get(id=task_id)
    task.title = payload.title
    task.description = payload.description
    task.completed = payload.completed
    task.save()
    return 204, None


@api.delete("/tasks/{task_id}", response={204: None})
def delete_task(request, task_id: int):
    """
    刪除一個任務
    """
    task = Task.objects.get(id=task_id)
    task.delete()
    return 204, None
