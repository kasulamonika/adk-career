-- RIASEC Assessment Questions Seed Data
-- R = Realistic, I = Investigative, A = Artistic, S = Social, E = Enterprising, C = Conventional

-- ========================
-- REALISTIC (R) Questions
-- ========================
INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('How do you prefer to solve a technical problem?',
 'R',
 'Read documentation and research online',
 'Try building a quick prototype',
 'Discuss with colleagues for ideas',
 'Draw diagrams and plan on paper',
 1, 4, 2, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('Which activity appeals to you the most?',
 'R',
 'Writing poetry or stories',
 'Assembling or repairing hardware',
 'Organizing a community event',
 'Analyzing stock market data',
 1, 4, 2, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('When given a new gadget, what do you do first?',
 'R',
 'Read the user manual thoroughly',
 'Take it apart to see how it works',
 'Ask a friend to show you how to use it',
 'Just start pressing buttons and explore',
 2, 4, 1, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('What type of project excites you?',
 'R',
 'Building a robot or IoT device',
 'Creating a mobile app UI design',
 'Conducting a scientific experiment',
 'Planning a marketing campaign',
 4, 2, 3, 1);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('In a team project, which role would you choose?',
 'R',
 'The person who builds and tests the product',
 'The person who designs the look and feel',
 'The person who presents to stakeholders',
 'The person who manages the schedule',
 4, 2, 1, 3);

-- ========================
-- INVESTIGATIVE (I) Questions
-- ========================
INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('How do you approach learning a new subject?',
 'I',
 'Watch video tutorials passively',
 'Deep-dive into research papers and books',
 'Learn by doing hands-on projects',
 'Join a study group and discuss',
 1, 4, 3, 2);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('What fascinates you the most?',
 'I',
 'Understanding how the universe works',
 'Creating beautiful artwork',
 'Helping people solve their problems',
 'Building a successful business',
 4, 1, 2, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('When you encounter a bug in code, what is your first instinct?',
 'I',
 'Google the error message immediately',
 'Methodically trace through the logic step by step',
 'Ask a senior developer for help',
 'Try random fixes until something works',
 2, 4, 1, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('Which career sounds most interesting?',
 'I',
 'Data Scientist analyzing complex datasets',
 'Graphic Designer creating brand identities',
 'Event Manager organizing conferences',
 'Sales Manager leading a team',
 4, 1, 2, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('What kind of books or articles do you enjoy reading?',
 'I',
 'Science and technology discoveries',
 'Fiction and creative writing',
 'Self-help and motivation',
 'Business and entrepreneurship',
 4, 1, 2, 3);

-- ========================
-- ARTISTIC (A) Questions
-- ========================
INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('How would you describe your ideal work environment?',
 'A',
 'A quiet lab with equipment',
 'A creative studio with freedom to experiment',
 'A busy office with lots of teamwork',
 'A structured corporate environment',
 2, 4, 3, 1);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('Which skill would you most like to develop?',
 'A',
 'Advanced mathematics',
 'UI/UX design and visual storytelling',
 'Public speaking and leadership',
 'Financial analysis and planning',
 2, 4, 3, 1);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('When presenting an idea, how do you prefer to communicate?',
 'A',
 'Through detailed written reports',
 'Through visual presentations with graphics and demos',
 'Through a passionate verbal pitch',
 'Through data charts and spreadsheets',
 2, 4, 3, 1);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('Which hobby resonates with you the most?',
 'A',
 'Solving puzzles and brain teasers',
 'Photography, painting, or music',
 'Volunteering and community service',
 'Playing competitive sports',
 2, 4, 3, 1);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('If you could create anything, what would it be?',
 'A',
 'A new scientific theory',
 'An innovative app with stunning design',
 'A non-profit organization',
 'A profitable startup company',
 2, 4, 3, 1);

-- ========================
-- SOCIAL (S) Questions
-- ========================
INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('What motivates you the most in your work?',
 'S',
 'Solving complex technical challenges',
 'Helping others succeed and grow',
 'Creating something new and beautiful',
 'Achieving targets and earning rewards',
 2, 4, 3, 1);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('How do you handle conflicts in a team?',
 'S',
 'Avoid them and focus on your work',
 'Mediate and find a compromise everyone agrees on',
 'Take charge and make the final decision',
 'Follow whatever the majority decides',
 1, 4, 2, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('Which role in education would you prefer?',
 'S',
 'Researcher in a university lab',
 'Teacher or mentor guiding students',
 'Administrative head of an institution',
 'Course designer creating curriculum',
 2, 4, 1, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('When a friend is struggling with a problem, you usually:',
 'S',
 'Give them space to figure it out',
 'Listen patiently and offer emotional support',
 'Give direct advice on what to do',
 'Help them create an action plan',
 1, 4, 2, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('What kind of impact do you want your career to have?',
 'S',
 'Advance scientific knowledge',
 'Improve people''s lives directly',
 'Create wealth and business growth',
 'Build reliable systems and infrastructure',
 2, 4, 1, 3);

-- ========================
-- ENTERPRISING (E) Questions
-- ========================
INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('How do you feel about taking risks?',
 'E',
 'I avoid risks and prefer safe choices',
 'I take calculated risks when the reward is high',
 'I love taking bold risks',
 'I only take risks when forced to',
 1, 3, 4, 2);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('In a group discussion, you tend to:',
 'E',
 'Listen quietly and observe',
 'Share ideas when asked',
 'Lead the conversation and propose directions',
 'Summarize what others have said',
 1, 2, 4, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('Which scenario excites you the most?',
 'E',
 'Discovering a new algorithm',
 'Pitching your startup to investors',
 'Designing a beautiful product',
 'Teaching a class of students',
 2, 4, 1, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('What is your approach to achieving goals?',
 'E',
 'Steady, consistent effort over time',
 'Set ambitious goals and push hard to achieve them',
 'Go with the flow and see what happens',
 'Plan meticulously before starting',
 2, 4, 1, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('How do you view competition?',
 'E',
 'It makes me uncomfortable',
 'It drives me to perform better',
 'I prefer collaboration over competition',
 'It depends on the situation',
 1, 4, 2, 3);

-- ========================
-- CONVENTIONAL (C) Questions
-- ========================
INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('How do you organize your daily tasks?',
 'C',
 'I keep a mental note and wing it',
 'I use detailed to-do lists and calendars',
 'I prioritize based on urgency as they come',
 'I delegate most tasks to others',
 1, 4, 3, 2);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('Which data-related task interests you?',
 'C',
 'Exploring data for hidden patterns',
 'Organizing and structuring messy data',
 'Visualizing data in creative charts',
 'Presenting data findings to executives',
 3, 4, 2, 1);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('What is your relationship with rules and processes?',
 'C',
 'I find them restrictive and limiting',
 'I follow them strictly and appreciate structure',
 'I follow them loosely as guidelines',
 'I create new rules when existing ones don''t work',
 1, 4, 2, 3);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('When working on a project, you prefer to:',
 'C',
 'Improvise and adapt as you go',
 'Follow a well-defined plan with clear milestones',
 'Work independently with minimal structure',
 'Brainstorm creatively without constraints',
 2, 4, 3, 1);

INSERT INTO riasec_questions (question_text, category, option_a, option_b, option_c, option_d, score_a, score_b, score_c, score_d) VALUES
('Which quality do you value most in yourself?',
 'C',
 'Creativity and imagination',
 'Attention to detail and accuracy',
 'Empathy and understanding',
 'Ambition and drive',
 1, 4, 2, 3);
