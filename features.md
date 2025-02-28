# 1.0 Schedule

# 2.0 Timer

# 3.0 Socrates AI
    #3.1 Prompt Engineering
        #3.1.1 Uses Socratic method to teach, when in study mode.
        #3.1.2 Uses 80/20 method. i.e the most important 20% that will help me understand 80% of the content. 
        #3.1.3 If need be it will use metaphors and stories to aid my memory
        #3.1.4 Could create roadmaps 
        #3.1.5 Will remind of projects that are not yet finished, to avoid having a backlog of projects that are incomplete.

# 4.0 OpenCV package to take in images
    contrast the image so more visible
    Tesseract with image_to_string function 
    Image is then fed into LLM, with an awaiting prompt to complete a certain instruction.

**DONE**
# 1.0
    * Summarization of prompts added and Session Manager done. the LLM gives a short summary of what was discussed. Saves tokens. Session Manager done. Session details are saved in a json file, each session with a timestamp (datetime.now()) and then summarized. The two go hand in hand. Summarization is done automatically when 75% of token limit is reached. 

    75% because, each summarization call costs tokens/ money and adds latency. Summarizing a 100 token convo wastes API calls for no reason. 
    Also, if the summaries are too basic, then over-summarizing could affect and skew the responses.  *important*

    This implies there is a token Buffer of 25%, reserving space for new user questions, AI responses, system messages.

    Its also more natural if there are about 10-15 exchanges before summarizing. 
    Short convos dont need summarizing, unless details are important, in which case i can just tell it to save. Long convos get summarized only when necessary.  

    MAX OF 4096 TOKENS PER REQUEST. What exactly is a request? it is a session ---
    Each API request includes the entire conversation history up to that point, so the token limit applies per request. If the accumulated tokens (system message + history + new question + response) exceed the model's limit, the request will fail. The 75% threshold is a precaution to start summarizing before hitting the limit.


    this currently reduces token usage by like 60% - 80% 

    Maybe next, it would be worth it to try embedding(instead of TF-DIF). 
# 2.0 Give Socrates Access to the date and time. So he has some perception of time. Shouldn't be too hard.  
    Later on, 
    deadline management for schedule
    Pomodoro Statistics tracking

    TimeZone Feature Done
    Benefits:
    Global usability (users in different timezones)
    Accurate deadline tracking across regions
    Consistent time references in summaries

    time is included in the summaries for better recollection.


    WOULD IT BE MORE EFFICIENT TO TIE THAT TO GEOLOCATION?


# 3.0 Give Socrates Memory
    If Socrates has memory I can continue building Socrates with Socrates. It would be fulfilling it's purpose
    Potential ways to enhance memory.
    * Token optimization - Only the relevant tokens are requested within each api request. 
    * TF-DIF - Instead of using this use embedding instead. Capture the semantic meaning instead, e.g "gravity" ~ "relativity". 
    * Summarization - Prioritize context, without saving the entire convo becasue this will save tokens.  Its an artificial brain, it will connect dots, because it has the underlying. Our brains do this too.
    * Session based storage - All the data from the session is grouped, perhaps for efficiency. This could be paired with the summarization technique and there could be a summarization for the whole session. 
    * Database - Using an unstructured database, e.g postSql or Mongo or Cassandra. What are the benefits to doing this? What is the difference if the tokesn are being counted from another place?
    * Layered Storage - Not all data is stored the same way. Data like my progress and my identity could be stored in a faster, more expensve form of data storage, in this case like my hard drive, while less frequently accessed data, like conversation data could be stored in the database or something. 

    Check the efficiency of each one by comparing to the efficiency of the prior method 

    Efficiency of Summarization - 50% - 80% 

    Summarization reduces tokens used per request, however increases processing time. The thng is already slow.


***TO DO**

# 1.0 Combine all the features 
    Later on, find a way to add all the features into one. I.E you can just enter a command to enter "add go to gym at 8pm to my schedule" or "turn on study mode. To do this, it would be preferable if the response time is faster. 


    

# 3.0 Give Socrates access to files in this directory
    This will allow it to see and keep track of files in directory as needed. It will not make any changes to the files (no idea how it would even do that). It should have access as this will make it easy to reference files when building projects. Maybe to start, it will be able to read files and later  on be able to write to different files and access different folders. Later on, it might have access to certain folders within the computer. 

# 4.0 Give Socrates the ability to browse the web and commplete    certain web related tasks. 

# 5.0 Some form of basic UI will be needed soon
    So that formulas can be displayed etc.

    #4.1 Image submission will  important as well. 



# 7.0 If theres a way to cache important information and give the LLM access to it at all times. Info that will be used often.  Sort of like summarization right?

# Potential Features
    *Encryption. Would it be wise to make the encryptions end to end? Would i want to have access to the users requests? It might be a good idea and they can use it to search hpotentially harmful things. At the same time the user has a right to their full privacy. Perhaps some holds on the degrees of freedom the AI is allowed to give the user access to, e.g no harmful content. This goes outside the bounds of encryption but is still useful to think about.  

# Access to system Files. 
    Will have read and writ access to this directory. It will be able to creat or make instances of files based on context. Based on commands, it woill contextually know to read or write or create files based on context 

# 8.0 Sound. Ability to give socrates vocal commands and have them executed. Learn how gpt does this. it will be key to giving it conversational ability. However before full conversational ability, it will need to be faster, i.e the calls and the execution. Will possibly need more threading for this feature as it will have to be listening for typed commands as well as recorded commands, maybe when a certain command is pressed, e,g "record" to start recording and "stoprec" to stop recording. 

# Access to browse the web. How does gpt and other LLMs do this?

# A sense of vision. Turn on System camera to see what is being shown, Maybe an interface for that so one can see what the AI will be seeing. OpenCV ?

# The AI will learn with me, so anything that I discover, that AI does not alreay know will be saved in summary, so for example in the process of learning something, we discover something like a new algorithm, that hasn't exactly been discovered yet. It could be a combo of algos that solves a certain task, or just an idea. This can be manually inputted into the summary. 

# Basic UI


# How would i turn socrates ai to my version of steven holstrom? Liek a holographic version of him or maybe with 

# Socrates willl be on all the time, listening in real time




UI Will be like a clone of gpt. How do i do this?

<!-- 
```python

def taste(sweets):
    sweet = True
    if sweets == sweet:
        return (f"the sweets are sweet")

``` -->


text to speech for socrates


