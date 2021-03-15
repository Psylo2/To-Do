from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, date

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def today_task():
    d = datetime.today()
    lt = session.query(Table).filter_by(deadline=datetime.today()).all()
    print(f"Today {d.day} {d.strftime('%b')}:")
    if not lt:
        print('Nothing to do!\n')
        menu()
    for x in lt:
        print(f"{lt.index(x)+1}. {x.task}")
    menu()


def add_task():
    print("Enter task")
    a = input()
    print("Enter deadline")
    d = datetime.strptime(input(), '%Y-%m-%d')
    new_row = Table(task=a, deadline=d)
    session.add(new_row)
    session.commit()
    print("The task has been added!\n")
    menu()


def weeks_task():
    for y in range(0, 7):
        d = datetime.today() + timedelta(days=y)
        formatted_date = date.strftime(d, '%Y-%m-%d')
        lt = session.query(Table).filter_by(deadline=formatted_date).all()
        print(f"{d.strftime('%A')} {d.day} {d.strftime('%b')}:")
        for x in lt:
            print(f"{lt.index(x) + 1}. {x.task}\n")
        if not lt:
            print('Nothing to do!\n')
    menu()


def all_tasks():
    lt = session.query(Table).order_by(Table.deadline).all()
    print("All tasks:")
    for x in lt:
        d = x.deadline
        print(f"{lt.index(x)+1}. {x.task}. {d.strftime('%d')} {d.strftime('%b')}")
    print("\n")
    menu()


def missed_tasks():
    lt = session.query(Table).filter(
        Table.deadline < datetime.today().date()).order_by(
        Table.deadline).all()
    print("Missed tasks:")
    if not lt:
        print('Nothing to do!\n')
    for x in lt:
        d = x.deadline
        print(f"{lt.index(x) + 1}. {x.task}. {d.strftime('%d')} {d.strftime('%b')}")
    print("\n")
    menu()


def delete_task():
    lt = session.query(Table).order_by(Table.deadline).all()
    print("Choose the number of the task you want to delete:")
    for x in lt:
        d = x.deadline
        print(f"{lt.index(x) + 1}. {x.task}. {d.strftime('%d')} {d.strftime('%b')}")
    if not lt:
        print("Nothing to delete\n")
        menu()
    num = int(input())
    z = session.query(Table).filter_by(id=lt[num-1].id).first()
    session.delete(z)
    session.commit()
    print("The task has been deleted!\n")
    menu()


def menu():
    print(f"1) Today's tasks\n"
          f"2) Week's tasks\n"
          f"3) All tasks\n"
          f"4) Missed tasks\n"
          f"5) Add task\n"
          f"6) Delete task\n"
          f"0) Exit"
          )
    a = int(input())
    if a == 1:
        today_task()
    elif a == 2:
        weeks_task()
    elif a == 3:
        all_tasks()
    elif a == 4:
        missed_tasks()
    elif a == 5:
        add_task()
    elif a == 6:
        delete_task()
    elif a == 0:
        print("Bye!")
        exit()
    else:
        print("invalid input\n")
        menu()


menu()