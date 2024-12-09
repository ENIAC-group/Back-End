#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import multiprocessing
from django.core.management import call_command
from django.core.management.commands.runserver import Command as RunServerCommand
# from django.core.management import execute_from_command_line

# def run_send_daily_message():
#     """Function to run the send_daily_message management command."""
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BackEnd.settings")
#     from django.core.management import call_command
#     call_command("start_bot")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BackEnd.settings")
    try:
        from django.core.management import execute_from_command_line
        # send_daily_message_process = multiprocessing.Process(target=run_send_daily_message)
        # send_daily_message_process.start()
        # execute_from_command_line(sys.argv)
        # send_daily_message_process.join()

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()



# class Command(RunServerCommand):
#     def handle(self, *args, **options):
#         # Define a function to run your management command
#         def run_tasks():
            
#             os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BackEnd.settings')
#             call_command('command')

#         # Create a separate process for running the management command
#         process = multiprocessing.Process(target=run_tasks)
#         process.start()

#         # Run the Django development server as usual
#         super().handle(*args, **options)

# if __name__ == "__main__":
#     from django.core.management import execute_from_command_line
#     os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BackEnd.settings")
#     print("lsjdfljflf")
#     execute_from_command_line(sys.argv)

