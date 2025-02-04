from schedule_manager import ScheduleManager
from study_mode import StudyModeController
from openai import OpenAI
from session_manager import SessionManager
from summarizer import Summarizer

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


    #Initialize with session management
    study_controller = StudyModeController(scheduler.client, user_id= "user123")

    #during operation
    study_controller.start_study_mode()

    #when session ends
    summary = study_controller.summarizer.summarize_conversation(study_controller.current_history)
    study_controller.session_manager.update_session_summary(summary)
    study_controller.session_manager.save_sessions

if __name__ == "__main__":
    main()