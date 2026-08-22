import mysql.connector


def save_report(user_goal, task, report, verification):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="agentx24"
    )

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_reports (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_goal TEXT,
            task VARCHAR(100),
            report LONGTEXT,
            verified BOOLEAN
        )
    """)

    cursor.execute("""
        INSERT INTO agent_reports
        (user_goal, task, report, verified)
        VALUES (%s, %s, %s, %s)
    """, (
        user_goal,
        task,
        report,
        verification["verified"]
    ))

    connection.commit()

    cursor.close()
    connection.close()