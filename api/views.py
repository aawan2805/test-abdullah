from django.shortcuts import render
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from api.models import Company
from api.serializer import CompanySerializer
import dateutil.parser

# Create your views here.
class CompanyView(APIView):
	def get(self, request, format=None):
		company_name = request.query_params.get('company', None)
		if company_name is not None and company_name == "fakeSolar":
			inspectors = requests.get('https://6244305b3da3ac772b0c7854.mockapi.io/fakeSolar/3rdParty/inspectors')
			inspections = requests.get('https://6244305b3da3ac772b0c7854.mockapi.io/fakeSolar/3rdParty/inspections')

			data = {
				"inspections": [],
			}
			total_warning_issues = 0
			total_critical_issues = 0
			for inspector in inspectors.json():
				# Filtramos todas las inspections para el inspector.
				for inspection in inspections.json():
					if str(inspection["inspectorId"]) == inspector["id"]:
						aux = {}
						# Date parsing.
						dt = inspection["scheduledDate"]
						dt = dateutil.parser.parse(dt)

						aux["title"] = f'{inspection["city"]} - {dt.year}/{dt.month}/{dt.day}'
						aux["inspectorName"] = inspector["name"]

						count_issues = 0
						count_warnings = 0
						for item in inspection["items"]:
							if item["isIssue"] and int(item["severity"]) < 60:
								count_warnings += 1
							elif item["isIssue"] and int(item["severity"]) >= 60:
								count_issues += 1

						aux["issuesWarningCount"] = count_warnings
						aux["issuesCriticalCount"] = count_issues
						aux["itemsOk"] = False if count_issues > 0 or count_warnings > 0 else True

						data["inspections"].append(aux)
						total_warning_issues += count_warnings
						total_critical_issues += count_issues
			data["total_warning_issues"] = total_warning_issues
			data["total_critical_issues"] = total_critical_issues

		else:
			serial = CompanySerializer(Company.objects.filter(company=company_name), many=True)
			data = serial.data

		return Response(data)
