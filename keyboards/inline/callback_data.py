from aiogram.utils.callback_data import CallbackData

change_city_callback = CallbackData("change_city")
get_release_calendar_callback = CallbackData("get_calendar")
check_pushkard_afisha_callback = CallbackData("check_pushkard_afisha")
add_favorites_callback = CallbackData("add_favorites")
favorite_movie_callback = CallbackData("favorite_movie_callback", "movie_id")
delete_favourite_movie_callback = CallbackData("delete_favourite_movie_callback", "movie_id")
get_afisha_movie_callback = CallbackData("get_afisha_movie_callback", "movie_id")
add_favorite_movie_callback = CallbackData("add_favorite_movie_callback", "movie_id")
get_soon_movie_callback = CallbackData("get_soon_movie_callback", "movie_id")
timetable_movie_callback = CallbackData("timetable_movie_callback", "movie_id")
change_notification_callback = CallbackData("change_notification_callback")
delete_notification_callback = CallbackData("delete_notification_callback")