import os

# Get the current working directory (where the script is executed)
current_directory = os.getcwd()


# Get the parent folder path
parent_folder = os.path.dirname(current_directory)

print(f"The parent folder path is: {parent_folder}")


# # Define the pattern to match child folders
# pattern = r"\migrations"

# # Walk through the parent folder and delete matching child folders
# for root, dirs, files in os.walk(parent_folder):
#     for dir_name in dirs:
#         if dir_name.endswith(pattern):
#             dir_path = os.path.join(root, dir_name)
#             try:
#                 os.rmdir(dir_path)
#                 print(f"Deleted directory: {dir_path}")
#             except OSError as e:
#                 print(f"Error deleting directory {dir_path}: {e}")

# print("Finished deleting directories.")

# import os

# # Define the parent folder path
# parent_folder = r"C:\path\to\parent_folder"

# # Define the command to run
# command = "python manage.py makemigrations"

# # List of app names
# app_names = ["accounts", "counseling", "reservation" , "Profile" , "GoogleMeet" , "reservation" , "telegrambot" , "TherapyTests"]

# # Iterate through app names and run the command
# for app_name in app_names:
#     app_path = os.path.join(parent_folder, app_name)
#     try:
#         os.chdir(app_path)  # Change to the app directory
#         os.system(command)  # Run the command
#         print(f"Command executed successfully for {app_name}.")
#     except OSError as e:
#         print(f"Error executing command for {app_name}: {e}")

# print("Commands executed successfully for all app directories.")
