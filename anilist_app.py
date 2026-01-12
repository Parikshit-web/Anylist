import csv
import os

def initialize_admin():
    if not os.path.exists("user.csv") or os.stat("user.csv").st_size == 0:
        with open("user.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([1, "Parikshit", "11", "admin"])
        print("Default admin created.")


def get_next_user_id():

    if not os.path.exists("user.csv") or os.stat("user.csv").st_size == 0:
        return 1
    
    with open("user.csv", "r") as file:
        rows = list(csv.reader(file))
        last_id = int(rows[-1][0])
        return last_id + 1
    

def create_user():
    with open("user.csv", "a", newline='') as file:
        user_id = get_next_user_id()
        username = input('enter name = ')
        password = input('enter password = ')
        role = input('enter role(admin/user) = ')
        row = [user_id, username, password,role]
        csvw = csv.writer(file)
        csvw.writerow(row)
    print("\n user created successfully...!!!\n")


def login():
    with open("user.csv", "r") as file:
        username = input('enter name = ')
        password = input('enter password = ')
        if not username or not password:
            print('Please fill in all fields')

        reader = csv.reader(file)
        for row in reader:
            if row[1] == username and row[2] == password:
                print("login successful")
                return row[0], row[3]
                
        print("invalid username or password")
        return None,None
    

def main():
    user_id, role = login()
    if user_id is None:
        return 
    if role == "admin":
        while True:
            print('Welcome User to Anilist')
            print("""MENU
            1.Admin Menu
            2.User Menu
            3.Exit
            """)
            choice=int(input('choose an option: '))

            if choice==1:
                admin_menu(user_id)

            elif choice==2:
                user_menu(user_id)
            else:
                break
    else:
        user_menu(user_id)

    
def get_next_watch_id():
    if not os.path.exists("watchlist.csv") or os.stat("watchlist.csv").st_size == 0:
        return 1

    with open("watchlist.csv", "r") as file:
        rows = list(csv.reader(file))
        return int(rows[-1][0]) + 1
    

def add_show(user_id):
    with open("watchlist.csv", "a", newline='') as file:
        watch_id=get_next_watch_id()
        show = input('enter show name = ')
        rating = int(input('enter rating = '))
        category = (input('enter category(W,C,P) = '))
        row = [watch_id,user_id,show, rating, category]
        csvw = csv.writer(file)
        csvw.writerow(row)
    print("\n show added successfully.\n")


def view_shows(user_id):
    search_show = input('enter show name = ')
    with open('watchlist.csv','r') as file:
        reader = csv.reader(file)
        found = False
        for row in reader:
            if row[1] == str(user_id) and row[2] == search_show:
                found = True
                print('Show =', row[2],'\nCategory =', row[4],'\nRating =', row[3])
        if not found:
            print('\nNo show record found.')



def display_all_shows(user_id):
    with open('watchlist.csv','r') as file:
        all_data=csv.reader(file)
        print('_'*30)
        for show in all_data:
            print('|\t',show[2],'\t|\t',show[3],'\t|\t',show[4],'\t|')
        print('\nAll Shows Records printed succesfully.\n')


def update_show(user_id):
    search_show = input("enter show name to update: ")
    updated_rows = []
    found = False

    with open("watchlist.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == str(user_id) and row[2] == search_show:
                print("1. Update category")
                print("2. Update rating")
                choice = input("choose option: ")
                if choice == "1":
                    new_category = input("enter new category: ")
                    row[4] = new_category
                elif choice == "2":
                    new_rating = input("enter new rating: ")
                    row[3] = new_rating
                found = True
            updated_rows.append(row)
    if not found:
        print("Show not found.")
        return

    with open("watchlist.csv", "w", newline="") as file:
        csv.writer(file).writerows(updated_rows)

    print("Show updated successfully.")



def delete_show(user_id):
    search_show = input("enter show name to delete: ")
    remaining_rows = []
    found = False

    with open("watchlist.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == str(user_id) and row[2] == search_show:
                found = True
                continue   # skip this row (delete)
            remaining_rows.append(row)
    if not found:
        print("Show not found.")
        return
    
    with open("watchlist.csv", "w", newline="") as file:
        csv.writer(file).writerows(remaining_rows)
    print("Show deleted successfully.")



def user_menu(user_id):
    while True:
        print('Welcome User to Anilist')
        print("""MENU
        1.Add Show
        2.View Show
        3.View All Shows
        4.Update Show
        5.Delete Show
        """)
        choice=int(input('choose an option: '))

        if choice==1:
            add_show(user_id)

        elif choice==2:
            view_shows(user_id)

        elif choice==3:
            display_all_shows(user_id)

        elif choice==4:
            update_show(user_id)

        elif choice==5:
            delete_show(user_id)

        else:
            print('You have entered wrong choice')
        repeat=input('Do you want to continue or not?(Y/N)...')
        if repeat=='N':
            break
    print('thank you, see you soon.')



def search_user():
    search_id = input('enter user id = ')
    with open('user.csv','r') as file:
        reader = csv.reader(file)
        found = False
        for row in reader:
            if row[0] == search_id:
                found = True
                print('User_ID =', row[0],'\nUser =',row[1],'\nRole =', row[3])
        if not found:
            print('\nNo user record found.')


def display_all_users():
    with open('user.csv','r') as file:
        all_data=csv.reader(file)
        print('_'*30)
        for user in all_data:
            print('|\t',user[0],'\t|\t',user[1],'\t|\t',user[3],'\t|')
        print('\nAll Users Records printed succesfully.\n')




def change_user_role():
    user_id = input("enter user id: ")
    if user_id == "1":
        print("Cannot change role of permanent admin.")
        return
    updated_rows = []
    found = False

    with open("user.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == user_id:
                print("Current role:", row[3])
                new_role = input("enter new role (admin/user): ")
                row[3] = new_role
                found = True
            updated_rows.append(row)

    if not found:
        print("User not found.")
        return

    with open("user.csv", "w", newline="") as file:
        csv.writer(file).writerows(updated_rows)

    print("User role updated successfully.")


def delete_user():
    search_user = input("enter user id to delete: ")
    if search_user == "1":
        print("Cannot delete permanent admin.")
        return

    remaining_rows = []
    found = False

    with open("user.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == search_user:
                found = True
                continue   # skip this row (delete)
            remaining_rows.append(row)
    if not found:
        print("User not found.")
        return
    
    with open("user.csv", "w", newline="") as file:
        csv.writer(file).writerows(remaining_rows)
    print("User deleted successfully.")


def admin_menu(user_id):
    while True:
        print('Welcome Admin to Anilist')
        print("""MENU
        1.Add User
        2.View User
        3.View All Users
        4.Update User
        5.Delete User
        """)
        choice=int(input('choose an option: '))

        if choice==1:
            create_user()

        elif choice==2:
            search_user()

        elif choice==3:
            display_all_users()

        elif choice==4:
            change_user_role()

        elif choice==5:
            delete_user()

        else:
            print('You have entered wrong choice')
        repeat=input('Do you want to continue or not?(Y/N)...')
        if repeat=='N':
            break
    print('thank you, see you soon.')


initialize_admin()

main()