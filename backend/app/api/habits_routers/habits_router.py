from fastapi import APIRouter

from app.api.habits_routers import (
    carry_over_habits_router,
    create_new_habit_router,
    edit_habit_router,
    get_reminders_router,
    get_habit_stats_router,
    list_habits_router,
    remove_habit_router,
    retrieve_habit_router,
    track_habit_completion_router,
)

main_habits_router = APIRouter(prefix="/habits", tags=["habits"])

main_habits_router.include_router(carry_over_habits_router.router)
main_habits_router.include_router(create_new_habit_router.router)
main_habits_router.include_router(edit_habit_router.router)
main_habits_router.include_router(get_reminders_router.router)
main_habits_router.include_router(get_habit_stats_router.router)
main_habits_router.include_router(list_habits_router.router)
main_habits_router.include_router(remove_habit_router.router)
main_habits_router.include_router(retrieve_habit_router.router)
main_habits_router.include_router(track_habit_completion_router.router)
