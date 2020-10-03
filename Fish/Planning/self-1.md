## Self-Evaluation Form for Milestone 1

### General 

We will run self-evaluations for each milestone this semester.  The
graders will evaluate them for accuracy and completeness.

Every self-evaluation will go out into your Enterprise GitHub repo
within a short time afrer the milestone deadline, and you will have 24
hours to answer the questions and push back a completed form.

This one is a practice run to make sure you get


### Specifics 


- does your analysis cover the following ideas:

  - the need for an explicit Interface specification between the (remote) AI 
    players and the game system?
  - *Answer:* Kind of - our analysis alludes to the idea that a specification would be needed to communicate with the airtower, which is charged with fielding players' requests (see Airtower section of our analysis). However, it fails to explicitly state the need for designing and documenting said interface specification.


  - the need for a referee sub-system for managing individual games
  - *Answer:* For the most part, yes. Our analysis speaks to the referee component in its role in managing the game (see 3rd paragraph of the Referee section in our analysis). However, our analysis fails to mention prospect of supporting multiple individual games, and instead focuses on the role the referee plays for a game of Fish in general.


  - the need for a tournament management sub-system for grouping
    players into games and dispatching to referee components
  - *Answer:* No, our analysis fails to document the need for a tournament management sub-system. On the other hand, it charges the referee with at least one role said sub-system would take on, namely handling user sign-ups (see 1st and 2nd paragraphs under the Referee section of our analysis).


- does your building plan identify concrete milestones with demo prototypes:

  - for running individual games
  - *Answer:* Yes, our 3rd and last milestone builds on top of the previous ones and entails the development of the outstanding components needed to run an individual game, albeit over the network.



  - for running complete tournaments on a single computer 
  - *Answer:* No. Our plan does not include a local version of the game.



  - for running remote tournaments on a network
  - *Answer:* Kind of - our 3rd milestone features a GUI demo to demonstrate the game being played over the network; however, it fails to account for the possiblity of multiple games being run in parallel and instead takes on a monolithic approach to tournaments (see Milestone 3 of our milestone plan).




- for the English of your memo, you may wish to check the following:

  - is each paragraph dedicated to a single topic? does it come with a
    thesis statement that specifies the topic?
  - *Answer:* Yes and for the most part. More specifically, the first paragraph under the Referee section of our system description is not headed with a thesis statement.



  - do sentences make a point? do they run on?
  - *Answer:* Yes, they do, and no they do not run on.



  - do sentences connect via old words/new words so that readers keep
    reading?
  - *Answer:* Yes, the word choice and structure of our writing is variegated, yet consistent enough, to compel the reader to keep reading.



  - are all sentences complete? Are they missing verbs? Objects? Other
    essential words?
  - *Answer:* Yes, they are complete and no, they are not missing any verbs, objects or **essential words**.


  - did you make sure that the spelling is correct? ("It's" is *not* a
    possesive; it's short for "it is". "There" is different from
    "their", a word that is too popular for your generation.)
  - *Answer:* Yes, we did.



The ideal feedback are pointers to specific senetences in your memo.
For PDF, the paragraph/sentence number suffices. 

For **code repos**, we will expect GitHub line-specific links. 


