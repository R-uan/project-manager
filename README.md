# 🛠️ Project Manager

An educational backend API for a project management system, inspired by tools like GitHub Projects. 
It enables users to create teams, organize tasks, and manage project workflows.
This project is built for learning purposes and is not intended to replace or compete with existing team management solutions.
The goal of this specific repository is to get used to Python's syntax as well as learning the framework Django.

### Django Concepts Checklist
- [x] Django Project Structure (Apps, Settings)
- [x] Django Database (Models, ORM, Migrations, Queries)
- [x] Django Routing (Endpoints, Parameters, Queries)
- [x] Django Rest Framework (Serializers, API)
- [x] Django Authentication (Jwt)
- [x] Django Testing Framework


### Project Views Checklist

#### Authentication
- [x] Generate Token
- [x] Refresh Token

#### Accounts
- [x] Create Account
- [ ] Get Account Details
- [x] Get (Owned) Organizations
- [ ] Update Details (email, name, GitHub, password)

#### Organizations
- [x] Projects: Get Organization's Projects (Authentication Based)
- [x] Organization Member Basic Operations (~~Add~~, ~~Find~~, ~~Remove~~) # [TESTED]
- [x] Organization Basic Operations (~~Create~~, ~~Find~~, ~~Update~~, ~~Delete~~) # [TESTED] (Need to create query)

#### Projects
- [x] Project Assignees Operations (Add, Remove)
- [x] Projects Basic Operations (~~Create~~, ~~Find~~, ~~Update~~, ~~Delete~~)

#### Teams
Should remove teams and assign members to projects directly