from src.aropenai_agents.components.pathology_agent import pathologist, AnalyzeTestResult, ReportData
from src.aropenai_agents import logger
import asyncio
from agents import Runner, Agent, trace, gen_trace_id

class LabAdmin:


    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        logger.info(f"Inside LabAdmin run method")
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting analysis...")
            logger.info(f"processed_report:{query}")
            analysis = await self.analyzeTestResult(processed_report = query)

            logger.info("Medical report saved as medical_report.md")
            yield "analysis done, genrerating report..."     
            search_results = await self.generateMedicalReport(report_analysis = analysis)
            yield search_results.markdown_report
            logger.info(f"saving the file in .md format")
            with open("resources/medical_report.md", "w", encoding="utf-8") as f:
                f.write(search_results.markdown_report)

            logger.info("Medical report saved as medical_report.md")


    async def analyzeTestResult(self, processed_report) -> str: 
        """Analyze the test results provided in {processed_report} and provide analysis"""
        logger.info(f"Inside method analyzeTestResult")
        
        input = f"test results: {processed_report}"
        try: 
            result = await Runner.run(
                pathologist, 
                input
            )
            return str(result.final_output)
        except Exception:
            return None


    async def generateMedicalReport(self, report_analysis ) -> ReportData:
        """Analyze the lab report provided in {processed_report} and provide analysis"""
        logger.info(f"loaded the processed_report")
        input = f"output from analyzeTestResult sub-routine: {report_analysis}"
        result = await Runner.run(
            pathologist, 
            input
        )
        logger.info("preparing report")
        return result.final_output_as(ReportData)
