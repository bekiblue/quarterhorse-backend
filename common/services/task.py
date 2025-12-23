from typing import Optional
from common.repositories.factory import RepositoryFactory, RepoType
from common.helpers.exceptions import APIException
from common.models.task import Task

class TaskService:

    def __init__(self, config):
        self.repository_factory = RepositoryFactory(config)
        self.task_repository = self.repository_factory.get_repository(RepoType.TASK)
        self.config = config

    def get_tasks_by_person_id(self, person_id: str, completed: Optional[bool] = None):
        """Retrieve all tasks for a specific user, optionally filtered by completion status"""
        query = {"person_id": person_id}
        if completed is not None:
            query["completed"] = completed
        
        tasks = self.task_repository.get_many(query)
        return tasks

    def get_task_by_id(self, entity_id: str, person_id: str):
        """Fetch a specific task by its ID"""
        task = self.task_repository.get_one({"entity_id": entity_id, "person_id": person_id})
        if not task:
            raise APIException("Task not found.")
        return task

    def save_task(self, task: Task):
        """Persist a new task or update an existing one"""
        task = self.task_repository.save(task)
        return task

    def delete_task(self, task: Task):
        """Permanently delete a task from the database"""
        self.task_repository.delete(task)