import sqlite3

db = sqlite3.connect('database.db')
cursor = db.cursor()

cursor.execute('''
    create table if not exists BedTable(
    BedID     INTEGER
        primary key autoincrement,
    RoomID    INTEGER not null
        references RoomTable,
    BedNumber INTEGER not null,
    BedStatus TEXT    not null);           
               ''')

cursor.execute('''
    create table if not exists BookingTable(
    BookingID   INTEGER
        primary key autoincrement,
    TaskID      INTEGER not null
        references TaskTable,
    UserID      INTEGER not null
        references UserTable,
    BookingDate TIMESTAMP default CURRENT_TIMESTAMP);           
               ''')

cursor.execute('''
    create table if not exists HouseTable(
    HouseID         INTEGER
        primary key autoincrement,
    HouseName       TEXT not null
        unique,
    HouseAddress    TEXT not null
        unique,
    HousePhone      TEXT not null
        unique,
    HouseEmail      TEXT not null
        unique,
    HouseSupervisor TEXT);          
               ''')

cursor.execute('''
    create table if not exists RoomTable(
    RoomID       INTEGER
        primary key autoincrement,
    RoomNumber   INTEGER not null,
    RoomType     TEXT    not null,
    RoomCapacity INTEGER not null,
    HouseID      INTEGER not null
        references HouseTable);           
               ''')

cursor.execute('''
    create table if not exists TaskTable(
    TaskID          INTEGER
        primary key autoincrement,
    TaskName        TEXT    not null,
    Capacity        INTEGER not null,
    DifficultyLevel TEXT    not null,
    Points          INTEGER not null);           
               ''')

cursor.execute('''
    create table if not exists UserRoleTable(
    RoleID   INTEGER
        primary key autoincrement,
    RoleName TEXT not null);           
               ''')



cursor.execute('''
create table if not exists UserTable(
    UserID           INTEGER
        primary key autoincrement,
    Username         VARCHAR(255) not null
        unique,
    Password         VARCHAR(255) not null,
    FirstName        VARCHAR(255) not null,
    LastName         VARCHAR(255) not null,
    DOB              DATE         not null,
    ContactNumber    TEXT         not null,
    RoleID           INTEGER      not null
        references UserRoleTable,
    EnrollmentStatus TEXT    default 'Not Enrolled',
    HouseID          INTEGER default NULL
        references HouseTable,
    Message          TEXT    default NULL,
    RoomID           INTEGER default NULL
        references RoomTable,
    BedID            INTEGER default NULL
        references BedTable);
''')