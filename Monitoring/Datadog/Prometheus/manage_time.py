from datetime import datetime, timedelta

# # Using current time
# ini_time_for_now = datetime.time(datetime.now())
#
# # printing initial_date
# print("initial_date", str(ini_time_for_now))
#
# # Calculating future dates
# # for two years
# future_date_after_2yrs = ini_time_for_now + \
#                          timedelta(days=730)
#
# future_date_after_2days = ini_time_for_now + \
#                           timedelta(days=2)
#
# # printing calculated future_dates
# print('future_date_after_2yrs:', str(future_date_after_2yrs))
# print('future_date_after_2days:', str(future_date_after_2days))


date_time_str = '08:15:27.243860'
date_time_obj = datetime.strptime(date_time_str, '%H:%M:%S.%f')

#print('Date:', date_time_obj.date())
print('Time:', date_time_obj.time())
#print('Date-time:', date_time_obj)