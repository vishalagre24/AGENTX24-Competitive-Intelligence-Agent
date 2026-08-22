import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="agentx24"
    )


def add_competitor(company_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO competitors (company_name)
        VALUES (%s)
        """,
        (company_name,)
    )

    conn.commit()

    # Verification
    cursor.execute(
        """
        SELECT company_name
        FROM competitors
        WHERE company_name = %s
        """,
        (company_name,)
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return f"✅ Verification Passed: {company_name} saved."

    return "❌ Verification Failed"


def show_competitors():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM competitors
        """
    )

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data