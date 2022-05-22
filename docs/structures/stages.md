# Define your own stage
- A stage is **a group of tasks**. You will define an **id (name)** and a **description** for this stage which represents this group of tasks. Also, your id **shouldn't contain special characters** (e.g. `$%^&-`), only **underline** (e.g. `_`) is permitted. 
- These tasks often **have same data goals** (e.g. webscrapping a website, calling a particular API), but you can define your own stages in your own way.
- When each stage finishes the tasks it contains, it would produce a single table to the sqlite file. You can see stage tables inside the sqlite file.
- If you concern a lot about data loss, we **strongly suggest** you to **cut your tasks into smaller stages (task groups)**.

## Structure Syntax
```yml
stages:
  - id: <stage name (identitcal) (required)>
    description: <stage description (optional)>
    tasks:
      ... 
```

## An Example
```yml
stages:
  - id: get_uk_airbnb_data 
    description: getting airbnb host listing data of uk 
    tasks:
      ... 
```
