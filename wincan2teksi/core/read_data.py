#!/usr/bin/env python
# coding: utf-8 -*-
# ...existing code...
from pathlib import Path
import sqlite3
import logging

from wincan2teksi.core.objects import Project, Section, Inspection, Observation

# codes which should not be imported by default
SkipCode = "BCD"


def __read_table(cursor: sqlite3.Cursor, table_name: str, where_clause: str = None):
    """Reads a table from the SQLite database and returns a list of dictionaries.
    Each dictionary represents a row in the table with column names as keys.
    """
    if where_clause:
        cursor.execute(f"SELECT * FROM {table_name} WHERE {where_clause}")
    else:
        cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]


def read_data(file_path: str) -> list[Project]:
    if not Path(file_path).exists():
        raise FileNotFoundError(f"File {file_path} does not exist.")

    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    project_data = __read_table(cursor, "PROJECT", "PRJ_Deleted IS NULL")
    projects = [Project.from_dict(data) for data in project_data]

    for project in projects:
        logging.info(f"Processing project: {project.name} (PK: {project.pk})")
        sections = __read_table(
            cursor, "SECTION", f"OBJ_Project_FK = '{project.pk}' AND OBJ_Deleted IS NULL"
        )
        for section_data in sections:
            section = Section.from_dict(section_data)
            logging.debug(
                f"Found section: {section.name} (PK: {section.pk}) in project {project.name}"
            )

            inspections = __read_table(
                cursor, "SECINSP", f"INS_Section_FK = '{section.pk}' AND INS_Deleted IS NULL"
            )
            if not inspections:
                logging.warning(
                    f"No inspections found for section {section.name} (PK: {section.pk}) in project {project.name}"
                )
                continue
            for inspection_data in inspections:
                inspection = Inspection.from_dict(inspection_data)
                logging.debug(
                    f"Found inspection: {inspection.name} (PK: {inspection.pk}) in section {section.name}"
                )

                observations = __read_table(
                    cursor,
                    "SECOBS",
                    f"OBS_Inspection_FK = '{inspection.pk}' AND OBS_Deleted IS NULL",
                )
                if not observations:
                    logging.warning(
                        f"No observations found for inspection {inspection.name} (PK: {inspection.pk}) in section {section.name}"
                    )
                    continue
                for observation_data in observations:
                    observation = Observation.from_dict(observation_data)
                    logging.debug(
                        f"Found observation in inspection {inspection.name} (PK: {inspection.pk})"
                    )
                    inspection.add_observation(observation)

                section.add_inspection(inspection)
            project.add_section(section)
        logging.info(f"Found {len(project.sections)} sections in project {project.name}")

    return projects
