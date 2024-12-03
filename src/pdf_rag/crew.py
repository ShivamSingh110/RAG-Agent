from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from pdf_rag.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
from crewai_tools import PDFSearchTool
tool = PDFSearchTool(pdf='NIPS-2017-attention-is-all-you-need-Paper.pdf')
# tool = PDFSearchTool(
#     config=dict(
#         llm=dict(
#             provider="ollama", 
#             config=dict(
#                 model="llama2",
#                 # temperature=0.5,
#                 # top_p=1,
#                 # stream=true,
#             ),
#         ),
#         embedder=dict(
#             provider="google",
#             config=dict(
#                 model="models/embedding-001",
#                 task_type="retrieval_document",
#                 # title="Embeddings",
#             ),
#         ),
#     )
# )


@CrewBase
class PdfRag():
	"""PdfRag crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def pdf_search_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['pdf_search_agent'],
			tools=[tool],
			verbose=True
		)

	@agent
	def reporting_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['reporting_analyst'],
			verbose=True
		)

	@task
	def pdf_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['pdf_research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PdfRag crew"""
		return Crew(
			agents=self.agents, 
			tasks=self.tasks, 
			process=Process.sequential,
			verbose=True,
			
		)
