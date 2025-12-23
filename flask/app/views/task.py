from flask import request
from flask_restx import Namespace, Resource

from app.helpers.response import get_success_response, validate_required_fields, get_failure_response, parse_request_body
from common.app_config import config
from common.helpers.exceptions import APIException
from app.helpers.decorators import login_required
from common.models.task import Task
from common.services import TaskService

task_api = Namespace('task', description="Task-related APIs")

# Request schema for creating tasks
CREATE_TASK_SCHEMA = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'description': {'type': 'string', 'default': ''}
    }
}

# Request schema for updating tasks
UPDATE_TASK_SCHEMA = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'description': {'type': 'string'},
        'completed': {'type': 'boolean'}
    }
}

@task_api.route('/')
class Tasks(Resource):

    @login_required()
    @task_api.expect(CREATE_TASK_SCHEMA)
    def post(self, person):
        """Add a new task to the user's task list"""
        try:
            parsed_body = parse_request_body(request, ['title', 'description'])
            validate_required_fields({'title': parsed_body.get('title')})
            
            task_service = TaskService(config)
            
            task = Task(
                person_id=person.entity_id,
                title=parsed_body['title'].strip(),
                description=(parsed_body.get('description') or '').strip(),
                completed=False
            )
            
            task = task_service.save_task(task)
            return get_success_response(
                message="Task created successfully.",
                task=task.as_dict()
            )
            
        except APIException as e:
            return get_failure_response(message=str(e), status_code=400)
        except Exception as e:
            from common.app_logger import logger
            import traceback
            logger.error(f"Error creating task: {str(e)}\n{traceback.format_exc()}")
            return get_failure_response(
                message="An error occurred while creating the task.",
                status_code=500
            )
    
    @login_required()
    def get(self, person):
        """List all tasks belonging to the current user with optional completion filter"""
        try:
            completed_param = request.args.get('completed')
            completed = None
            
            if completed_param is not None:
                # Check and transform boolean query parameter
                if completed_param.lower() not in ('true', 'false'):
                    return get_failure_response(
                        message="Invalid 'completed' parameter. Must be 'true' or 'false'.",
                        status_code=400
                    )
                completed = completed_param.lower() == 'true'
            
            task_service = TaskService(config)
            tasks = task_service.get_tasks_by_person_id(person.entity_id, completed=completed)
            
            return get_success_response(tasks=[task.as_dict() for task in tasks])
            
        except APIException as e:
            return get_failure_response(message=str(e), status_code=400)
        except Exception as e:
            from common.app_logger import logger
            import traceback
            logger.error(f"Error fetching tasks: {str(e)}\n{traceback.format_exc()}")
            return get_failure_response(
                message="An error occurred while fetching tasks.",
                status_code=500
            )

@task_api.route('/<string:task_id>')
class TaskDetail(Resource):
    
    @login_required()
    def get(self, task_id, person):
        """Retrieve details of a specific task"""
        try:
            if not task_id:
                return get_failure_response(
                    message="Task ID is required.",
                    status_code=400
                )
            
            task_service = TaskService(config)
            task = task_service.get_task_by_id(task_id, person.entity_id)
            return get_success_response(task=task.as_dict())
            
        except APIException as e:
            return get_failure_response(message=str(e), status_code=400)
        except Exception as e:
            from common.app_logger import logger
            import traceback
            logger.error(f"Error fetching task: {str(e)}\n{traceback.format_exc()}")
            return get_failure_response(
                message="An error occurred while fetching the task.",
                status_code=500
            )


    @login_required()
    def delete(self, task_id, person):
        """Remove a task from the user's task list"""
        try:
            if not task_id:
                return get_failure_response(
                    message="Task ID is required.",
                    status_code=400
                )
            
            task_service = TaskService(config)
            task = task_service.get_task_by_id(task_id, person.entity_id)
            task_service.delete_task(task)
            
            return get_success_response(message="Task deleted successfully.")
            
        except APIException as e:
            return get_failure_response(message=str(e), status_code=400)
        except Exception as e:
            from common.app_logger import logger
            import traceback
            logger.error(f"Error deleting task: {str(e)}\n{traceback.format_exc()}")
            return get_failure_response(
                message="An error occurred while deleting the task.",
                status_code=500
            )


    @login_required()
    @task_api.expect(UPDATE_TASK_SCHEMA)
    def put(self, task_id, person):
        """Modify an existing task"""
        try:
            if not task_id:
                return get_failure_response(
                    message="Task ID is required.",
                    status_code=400
                )
            
            parsed_body = parse_request_body(request, ['title', 'description', 'completed'])
            
            task_service = TaskService(config)
            task = task_service.get_task_by_id(task_id, person.entity_id)
            
            # Apply updates to task fields
            updated = False
            if parsed_body.get('title'):
                task.title = parsed_body['title'].strip()
                updated = True
            if 'description' in parsed_body:
                task.description = (parsed_body.get('description') or '').strip()
                updated = True
            if 'completed' in parsed_body:
                task.completed = bool(parsed_body['completed'])
                updated = True
            
            if not updated:
                return get_failure_response(
                    message="At least one field must be provided for update.",
                    status_code=400
                )
            
            task = task_service.save_task(task)
            return get_success_response(
                message="Task updated successfully.",
                task=task.as_dict()
            )
            
        except APIException as e:
            return get_failure_response(message=str(e), status_code=400)
        except Exception as e:
            from common.app_logger import logger
            import traceback
            logger.error(f"Error updating task: {str(e)}\n{traceback.format_exc()}")
            return get_failure_response(
                message="An error occurred while updating the task.",
                status_code=500
            )

