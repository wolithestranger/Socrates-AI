from schedule_manager import ScheduleManager
from study_mode import StudyModeController
from openai import OpenAI

def main():
    #init system components 
    scheduler = ScheduleManager()
    study_controller = StudyModeController(scheduler.client)

    # Collect tasks and generate schedule
    scheduler.collect_additional_tasks()
    
    scheduler.generate_schedule()  # Generate the schedule first
    schedule = scheduler.generated_schedule  # Access the attribute

    print("\nGenerated Schedule: ")
    print(schedule)

    #start study mode if requested 
    if input("\nStart study mode? (yes/no): ").lower() == 'yes':
        study_controller.start_study_mode()

if __name__ == "__main__":
    main()