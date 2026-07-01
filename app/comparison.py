class AssessmentComparer:

    def compare(self, assessments):

        if len(assessments) < 2:
            return (
                "I need at least two assessments "
                "to perform a comparison."
            )

        reply = "# Assessment Comparison\n\n"

        for assessment in assessments:

            reply += f"""
## {assessment.get("name")}

Description:
{assessment.get("description")}

Duration:
{assessment.get("duration")}

Job Levels:
{assessment.get("job_levels_raw")}

Languages:
{assessment.get("languages_raw")}

Categories:
{", ".join(assessment.get("keys", []))}

URL:
{assessment.get("link")}

----------------------------------------

"""

        reply += """
Summary:

• Compare the assessments based on purpose.

• Choose according to hiring needs.

• All information above comes directly from the SHL catalog.
"""

        return reply