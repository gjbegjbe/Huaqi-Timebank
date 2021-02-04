import json
import pymysql

conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='root',
    db='time_bank',
    charset='utf8mb4'
)

cur = conn.cursor()

# TODO 部署时
path = ''

path_missions = r"技能与任务值参考.json"
f_missions = open(path+path_missions, "r", encoding='UTF8')
out_missions = f_missions.read()
dic_missions = json.dumps(out_missions)
dic_missions = json.loads(out_missions)
flat_dic_missions = {}
for item in dic_missions:
    for iitem in dic_missions[item]:
        flat_dic_missions[iitem] = dic_missions[item][iitem]

for mission in flat_dic_missions:
    sql_insert_mission = "insert into mission (id,name) values (" + "'" + str(
        flat_dic_missions[mission]) + "'" + "," + "'" + mission + "'" + ");"
    cur.execute(sql_insert_mission)

path_schools = r"大学值参考.json"
f_schools = open(path+path_schools, "r", encoding='UTF8')
out_schools = f_schools.read()
dic_schools = json.dumps(out_schools)
dic_schools = json.loads(out_schools)
for item in dic_schools:
    sql_insert_school = "insert into school (id,name) values (" + "'" + str(
        dic_schools[item]) + "'" + "," + "'" + item + "'" + ");"
    cur.execute(sql_insert_school)

path_generated_users = r"generated_users.json"
f_generated_users = open(path+path_generated_users, "r", encoding='UTF8')
out_generated_users = f_generated_users.read()
dic_generated_users = json.dumps(out_generated_users)
dic_generated_users = json.loads(out_generated_users)
num_generated_users = len(dic_generated_users)

for i in range(num_generated_users):
    user_id = dic_generated_users[i]['user_id']
    skills = dic_generated_users[i]['skills']
    education_level = dic_generated_users[i]['education_level']
    school_id = dic_generated_users[i]['school_id']
    finished_missions = dic_generated_users[i]['finished_missions']
    prepared_missions = dic_generated_users[i]['prepared_missions']
    print(str(user_id) + ' ' + str(skills) + ' ' + str(education_level) + ' ' + str(school_id)
          + ' ' + str(finished_missions) + ' ' + str(prepared_missions))
    sql_insert_user = "insert into user (id,schoolId,educationLevel) values (" + "'" + str(
        user_id) + "'" + "," + "'" + str(school_id) + "'" + "," + "'" + str(education_level) + "'" + ");"
    cur.execute(sql_insert_user)

    for skill in skills:
        sql_insert_skills = "insert into userskills (userId,missionId) values (" + "'" + \
                            str(user_id) + "'" + "," + "'" + str(flat_dic_missions[skill]) + "'" + ");"
        cur.execute(sql_insert_skills)

    for finished_mission in finished_missions:
        sql_insert_finished_mission = "insert into finishedmission (userId,missionId,times) values (" + "'" + \
                                      str(user_id) + "'" + "," + "'" + str(finished_mission) + "'" + "," \
                                      + "'" + str(finished_missions[finished_mission]) + "'" + ");"
        cur.execute(sql_insert_finished_mission)

    for prepared_mission in prepared_missions:
        sql_insert_prepared_mission = "insert into preparedmission (userId,missionId,times) values (" + "'" + \
                                      str(user_id) + "'" + "," + "'" + str(prepared_mission) + "'" + "," \
                                      + "'" + str(prepared_missions[prepared_mission]) + "'" + ");"
        cur.execute(sql_insert_prepared_mission)

conn.commit()
conn.close()
