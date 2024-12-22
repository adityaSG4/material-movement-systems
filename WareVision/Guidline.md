Team Guide for Project "VISION"

1. Introduction

    Project Name: "VISION"

    Project Goal: To develop an innovative, real-time warehouse automation system that uses computer vision, path planning, and an intuitive user interface.

    Problem Statement: To automate the process of guiding forklifts in a warehouse using AI and CAD/BIM tools.

    Our approach: Our approach will be to develop a computer vision based system that detects and labels all of the objects, and plans and executes a path using the information it gets from the computer vision.

    Why This Project Matters:

        Addresses real-world challenges in warehouse logistics.

        Offers practical, innovative solutions.

        Provides a platform for the team to develop advanced technical skills.

2. Core Project Components

    2.1. Perception (Computer Vision):

        Description: Using a mobile camera to capture the warehouse environment, and then using AI to detect objects.

        Tasks:

            Acquiring video feed from a mobile camera.

            Detecting and identifying boxes, obstacles, and other important objects with ArucoIDs.

            Extracting object positions, orientations, and other relevant data.

        Technology: OpenCV, YOLOv8.

    2.2. Navigation (Path Planning):

        Description: Designing algorithms for the robot to navigate from its current position to the destination.

        Tasks:

            Creating a map of the warehouse environment from the computer vision output.

            Implementing the A* algorithm to plan the shortest, safest path.

            Adapting to dynamic changes in the environment.

        Technology: A* Algorithm, Grid systems.

    2.3. Interaction (User Interface):

        Description: Create a user-friendly GUI for operators to interact with the robot.

        Tasks:

            Displaying the video stream, objects, and path.

            Providing buttons for starting and stopping the robot operation.

            Displaying data related to the operation of the robot.

        Technology: PyQt.

    2.4 CAD Modeling:

        Description: Design a CAD model for the robot and all of the mechanical parts that are used for the solution.

        Tasks:
        * Use a CAD program like Onshape to design your model.

        Technology: Onshape (or any other CAD software).

    2.5. System Integration:

        Description: Connecting all of the different parts to make a cohesive system.

        Tasks:

            Ensure data is transferred efficiently between all components of the system.

            Make sure that there are no bugs in the communication pipeline.

        Technology: Python based communication libraries.

    2.6. Presentation:

        Description: Show your solution to the judges.

        Tasks:

            Create a compelling presentation with a clear narrative.

            Provide sufficient information to judges for them to make informed decisions.

        Technology: Presentation software.

3. Team Roles and Responsibilities (Example)

    (Team Member 1 Name):

        Primary Focus: Computer Vision (Object Detection, Data Extraction)

        Secondary Focus: System Integration

    (Team Member 2 Name):

        Primary Focus: Path Planning (Algorithm Development, Optimization)

        Secondary Focus: CAD modeling.

    (Team Member 3 Name):

        Primary Focus: User Interface (Design and Implementation)

        Secondary Focus: Presentation.

    (Team Member 4 Name):

        Primary Focus: AI/ML and Model optimization.

        Secondary Focus: System Integration.

    (Note: Adjust team member names and roles based on your team structure and skills.)

4. Development Process

    Iterative Development: We will develop the software in iterations, focusing on one component at a time, testing, and refining.

    Version Control: All team members must be using git. All code should be pushed to github frequently.

    Code Quality: Keep all of your code clean, and easily understandable. Use comments and document important parts of the code.

    Collaboration: Be open to feedback, share your ideas, and collaborate effectively.

5. Technology Stack

    Programming Language: Python 3.8 or higher.

    Computer Vision: OpenCV.

    AI/ML: YOLOv8, PyTorch.

    User Interface: PyQt.

    Version Control: Git.

    CAD: Onshape (or any other CAD software).

6. Key Goals for Each Team Member

    Computer Vision Team Member: Focus on real-time detection, accurate extraction of object data, and working with the YOLOv8 model.

    Path Planning Team Member: Create an efficient algorithm that handles obstacles, and prioritize shortest path, and real time changes.

    User Interface Team Member: Develop an intuitive, easy-to-use, and visually appealing interface.

    AI/ML Team Member: Focus on making the AI model accurate, efficient, and robust.

    CAD modeling team member: Focus on innovative mechanical design that has real world application.

7. Communication

    Regular team meetings to track progress, discuss challenges, and share new ideas.

    Use a communication platform (e.g., Slack, Discord) for quick updates.

8. How to "Win"

    Prioritize quality: A well-made and accurate product is more important than a complex product.

    Focus on innovation: Create a system that is novel and innovative.

    Real world application: Show that your system can be used in a real world scenario, and it can solve some very important problems.

    Good presentation: A well made presentation can add a lot of value to your solution.




######################################################################################################

(Team Member 1 - You (with complex understanding)):

    Primary Focus: Project Lead, System Integration, Core Algorithm Development

        Responsibilities:

            Oversee the entire project, ensuring all parts are integrated and working correctly.

            Design the core path planning logic and integrate it with all modules.

            Address any complex system-level issues that may arise.

            Provide training to other team members and help them whenever required.

            Make all architectural decisions

    Secondary Focus: AI/ML Model Refinement

        Responsibilities:

            Refine the AI model based on the output from other team members.

(Team Member 2 - New Team Member):

    Primary Focus: Computer Vision (Object Detection, Data Extraction)

        Responsibilities:

            Implement code to detect objects using OpenCV, and Aruco Markers.

            Extract object data (coordinates, orientation, etc.) and prepare for path planning.

            Work with the project lead to solve any issues that might arise while working with object detection.

            Debug and resolve any issues related to sensor data.

    Secondary Focus: User Interface (Basic design and integration)

        Responsibilities

            Develop a basic UI for all the modules based on project requirements.

(Team Member 3 - New Team Member):

    Primary Focus: User Interface (Design and Implementation)

        Responsibilities:

            Design the UI for clarity and easy usage.

            Work with the project lead to improve the design and implementation of the UI.

    Secondary Focus: Presentation

        Responsibilities

            Create a structured presentation outline and work with the project lead for the presentation.

(Team Member 4 - New Team Member):

    Primary Focus: CAD Modeling

        Responsibilities:

            Create CAD models for the robot and any mechanical system that are used for the operation.

    Secondary Focus: Presentation

        Responsibilities

            Assist with the presentation with design and visuals.