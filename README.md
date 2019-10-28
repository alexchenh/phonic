# phonic
## Inspiration
We were inspired by the "enhancement approach" described in the paper, "Teaching in low-resource classrooms: voices of experience" by the British Council. Rather than making a solution on the basis of our preconceived notions on what students and teachers should be doing, we read about the success stories of teachers in low-resource classrooms, and used that as the basis for our ideation. We found many success stories involved teachers leveraging group activities, discussions, and peer learning to nurture a sense of learning among students and teach effectively without access to many resources. Focusing on helping teachers exercise their human strengths, we wanted to create a tool for teachers to use during discussions that would allow them to spend less time recording speaking times, notes, etc., and more time facilitating successful group interaction and engaging discussion. 

## What it does
Phonic allows a teacher to start recording and focus solely on moderating and facilitating a great discussion. Our app will convert the audio file into key metrics and condensed summaries, allowing the teacher to look back and view discussion topics, important keywords, positive/negative sentiments, disagreement scores, and speakers and how long they spoke. This information will all be displayed in a highly visual, easy to understand dashboard.

## How we built it
Phonic takes an audio file, and feeds it to both Google's Speech to Text API as well as our own custom model built using TensorFlow to identify individual speakers and the amount of time they are speaking during the recording. The transcript file is analyzed using Google's NLP API to get sentiment analysis, and we used a separate library for keyword extraction. All of the data from our models is displayed using Flask as our web framework. 

## Challenges we ran into
None of us really have a grasp of the entire (huge) tech stack to build this, so it was a challenge to learn enough to implement so many different features. 

## Accomplishments that we're proud of
Doing something in edtech like we had hoped!

## What we learned
Delegating tasks, organizing our plan of action and diagraming our system helped a ton.

## What's next for phonic
Who said only schools have discussions? We're thinking of applications in business meetings, debates, and more!
