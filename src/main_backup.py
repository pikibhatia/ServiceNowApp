import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.express as px

# Placeholder for ServiceNow API class (to be customized with actual API calls)
class ServiceNowAPI:
    def __init__(self):
        self.base_url = "https://abbottprod.service-now.com/api/now/table"
        self.auth = ("SVC-SNOW-RPA-BOTS", "o*HbmD0xN9cW~hP2$rd<3].s>[{%v^TU")

    def fetch_data(self, table_name, query_params=None):
        if query_params==None:
            url = f"{self.base_url}/{table_name}"
        else:
            url = f"{self.base_url}/{table_name}{query_params}"
        headers = {"Accept": "application/json"}
        # st.write(url)
        response = requests.get(url, headers=headers, auth=self.auth, params=query_params)
        if response.status_code == 200:
            # st.write(response.json())
            return response.json().get("result", [])
        else:
            st.error(f"Failed to fetch data from {table_name}: {response.status_code}")
            return []

    def get_incidents(self, start_date, end_date, assignment_group):
        query = f"^opened_at>={start_date}^opened_at<={end_date}^{assignment_group}"
        # st.write(query)
        return self.fetch_data("incident", f"?sysparm_fields=state,short_description,business_service.name,number,priority,u_prob_type,category,assignment_group.name,sys_created_on,opened_at,closed_at,closed_by.employee_number,closed_by.user_name,closed_by.name,assigned_to.employee_number,assigned_to.user_name,assigned_to.name,sys_updated_on,priority,impact&sysparm_limit=30000&sysparm_query=assignment_group.u_provider_rollup=IBM{query}")

    def get_service_requests(self, start_date, end_date, assignment_group):
        query = f"^opened_at>={start_date}^opened_at<={end_date}^{assignment_group}"
        return self.fetch_data("sc_request", f"?sysparm_query=state,short_description,business_service.name,number,priority,u_prob_type,category,assignment_group.name,sys_created_on,opened_at,closed_at,closed_by.employee_number,closed_by.user_name,closed_by.name,assigned_to.employee_number,assigned_to.user_name,assigned_to.name,sys_updated_on,priority,impact&sysparm_limit=30000&sysparm_query=assignment_group.u_provider_rollup=IBM{query}")

    def get_problems(self, start_date, end_date):
        query = f"^opened_at>={start_date}^opened_at<={end_date}"
        return self.fetch_data("problem", "?sysparm_query=sys_created_on"+query)

    def get_slas(self):
        return self.fetch_data("task_sla")

    def get_assignment_groups(self):
        return self.fetch_data("sys_user_group", f"?sysparm_query=u_provider_rollup=IBM")

    def get_business_apps(self):
        return self.fetch_data("cmdb_ci_business_app")

# Streamlit UI Setup
st.set_page_config("ServiceNow Dashboard", layout="wide")
st.title("📊 ServiceNow Analytics Dashboard")

api = ServiceNowAPI()

# Date range inputs
date_col1, date_col2 = st.columns(2)
with date_col1:
    input_start_date = st.date_input("Start Date", datetime.now())
    start_datetime = datetime.combine(input_start_date, datetime.min.time())
    start_date= start_datetime.strftime("%Y-%m-%d %H:%M:%S")
with date_col2:
    input_end_date = st.date_input("End Date", datetime.now())
    end_datetime = datetime.combine(input_end_date, datetime.max.time())
    end_date= end_datetime.strftime("%Y-%m-%d %H:%M:%S")

st.markdown("---")

tabs = st.tabs(["Incidents", "Service Requests", "Problems", "SLAs", "Assignment Groups", "Business Apps"])

with tabs[0]:
    st.header("Incidents")
    col1,col2 = st.columns(2)
    with col1:
        options = ["All", "ANI-LATAM", "BPCS", "Collaboration", "DBA", "Finance", "Integration", "Legacy ERP", "Manufacturing", "Quality", "SAP"]
        selected = st.selectbox("Choose an option:", options, index=0)
    with col2:
        priorityoptions = ["All", "1", "2", "3", "4"]
        priorityselected = st.selectbox("Select Priority:", priorityoptions)
    if st.button("Load Incidents"):        
        if selected=="ANI-LATAM":
            assignment_group_params = "assignment_group.nameINANI-LATAM-AppSpprt-Nutritional Connection,ANI-LATAM-AppSpprt-LATAM Marketing Cloud,ANI-LATAM-AppSpprt-Pitcher Meteoro,ANI-LATAM-AppSpprt-LATAM Salesforce Service Cloud,ANI-LATAM-AppSpprt-LATAM Verify,ANI-LATAM-AppSpprt-Message Bird,ANI-LATAM-AppSpprt-Contigo Loyalty"
        if selected=="BPCS":
            assignment_group_params = "assignment_group.nameINIBM-EMEA-AppSpprt-ME-Critical App Support,IBM-APAC-AppSpprt-BPCS-5.1,IBM-EMEA-AppSpprt-ES-Access Administration Critical App Support,IBM-LATAM-AppSpprt-Finance BPCS Critical App Support,IBM-APAC-AppSpprt-Indonesia-Gold,IBM-GLOBAL-AppSpprt-Thenon Admin Support,IBM-EMEA-AppSpprt-FR-Critical Application Support,IBM-EMEA-AppSpprt-BE-Critical Application Support,IBM-EMEA-AppSpprt-EG-Critical App Support,IBM-EMEA-AppSpprt-TR-Finance Critical App Support,IBM-EMEA-AppSpprt-SA-Critical App Support,IBM-EMEA-AppSpprt-TR-Finance Non-Critical App Support,IBM-EMEA-AppSpprt-GPO-Zwolle-Business Applications,IBM-EMEA-AppSpprt-ZA-Critical App Support,IBM-APAC-AppSpprt-Malaysia-Gold,IBM-EMEA-AppSpprt-NL-BPCS Zwolle Support,IBM-EMEA-AppSpprt-IT-Non-Critical Application Support,IBM-EMEA-AppSpprt-PL-Non Critical Application Support,IBM-APAC-AppSpprt-China-Gold,IBM-EMEA-AppSpprt-IT-Critical Application Support,IBM-EMEA-AppSpprt-ES-Maintenance Non-Critical App Support,IBM-APAC-AppSpprt-Vietnam-Gold,IBM-EMEA-AppSpprt-ES-Maintenance Critical App Support,IBM-APAC-AppSpprt-Philippines-Gold"
        if selected=="Collaboration":
            assignment_group_params = "assignment_group.nameINIBM-GLOBAL-AppSpprt-ALM Services,IBM-GLOBAL-Appspprt-ColTech-Critical Commercial Digital,IBM-GLOBAL-Appspprt-ColTech-Critical IICS,IBM-GLOBAL-Appspprt-ColTech-Critical Intranet Websites,IBM-GLOBAL-Appspprt-ColTech-Critical Notes,IBM-GLOBAL-Appspprt-ColTech-Critical Other Ent Functions,IBM-GLOBAL-Appspprt-ColTech-Critical SharePoint,IBM-GLOBAL-Appspprt-ColTech-FoF App Support,IBM-GLOBAL-Appspprt-ColTech-FoF Intranet Websites,IBM-GLOBAL-Appspprt-ColTech-FoF Notes App Support,IBM-GLOBAL-Appspprt-ColTech-FoF Other Ent Functions App Support,IBM-GLOBAL-Appspprt-ColTech-FoF SharePoint,IBM-GLOBAL-Appspprt-ColTech-Intranet Websites,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Commercial,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Commercial Digital,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Commercial SFDC,IBM-GLOBAL-AppSpprt-ColTech-Non-Critical Content Mgmt,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Finance,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Human Resources,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Information Management,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Intranet Websites,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Manufacturing,IBM-GLOBAL-Appspprt-ColTech-Non-Critical MSPS Support,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Notes,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Other Ent Functions,IBM-GLOBAL-Appspprt-ColTech-Non-Critical PIM,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Salesforce Veeva Apps,IBM-GLOBAL-Appspprt-ColTech-Non-Critical SharePoint,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Technology,IBM-Global-AppSpprt-MEDDEV-Non-Critical-WebApplications"
            # assignment_group_params = urllib.parse.quote(",".join(assignment_group_params))
        if selected=="DBA":
            assignment_group_params = "assignment_group.nameINIBM-GLOBAL-DBA-MYSQL,IBM-GLOBAL-DBA-TLE AHD,IBM-GLOBAL-DBA-WWOps DBA Oracle,IBM-GLOBAL-DBA-CCI,IBM-GLOBAL-DBA-HR DB CHR,IBM-GLOBAL-DBA-CHAD Kronos,IBM-GLOBAL-DBA-ISTP Abbott,IBM-GLOBAL-DBA-Operations Oracle,IBM-GLOBAL-DBA-Informatica,IBM-GLOBAL-DBA-Enterprise DBA Operations Oracle,IBM-GLOBAL-DBA-Autosys,IBM-GLOBAL-DBA-QSDW,IBM-GLOBAL-DBA-ITSM GIS,IBM-GLOBAL-DBA-DCFL ANI,IBM-GLOBAL-DBA-SQL Server,IBM-GLOBAL-DBA-SAP MD DBA Oracle,IBM-GLOBAL-DBA-TIBCO GIS,IBM-GLOBAL-DBA-Shape,IBM-GLOBAL-DBA-GES MXES,IBM-GLOBAL-DBA-Supermaster,IBM-GLOBAL-DBA-SCMStaging ANI,IBM-GLOBAL-DBA-QC,IBM-GLOBAL-DBA-EDW,IBM-GLOBAL-DBA-TCGM,IBM-GLOBAL-DBA-ADD LIMS QIMS"
        if selected=="Finance":
            assignment_group_params = "assignment_group.nameINIBM-GLOBAL-Appspprt-Fin-Non-Critical Salesforce Veeva Apps,IBM-AMER-AppSpprt-CA-JDE Critical App Support,IBM-GLOBAL-AppSpprt-HQ Financial Critical Applications,IBM-GLOBAL-AppSpprt-OLAP Cube,IBM-LATAM-AppSpprt-ADAM,IBM-GLOBAL-AppSpprt-QSDW Level 2,IBM-GLOBAL-Appspprt-Fin-Non-Critical Cognos Planning Reporting ETL,IBM-GLOBAL-AppSpprt-EIMS SCR COGNOS CRITICAL APP SUPPORT,IBM-LATAM-AppSpprt-Brazil-Symphony BoltOn App Support,IBM-GLOBAL-Appspprt-Fin-Critical MES DRP iSeries,IBM-GLOBAL-AppSpprt-CCI Application Engineering,IBM-GLOBAL-AppSpprt-XMS Financial Solutions,IBM-GLOBAL-AppSpprt-APT,IBM-GLOBAL-AppSpprt-EIMS SCR WEB CRITICAL APP SUPPORT,IBM-GLOBAL-Appspprt-Fin-Non-Critical Microsoft COTS,IBM-GLOBAL-AppSpprt-Critical GRC Access Control,IBM-GLOBAL-AppSpprt-AN FC-Finance and HR Support,IBM-GLOBAL-AppSpprt-OnBase OCR Brainware,IBM-GLOBAL-AppSpprt-Hyperion SHAPE,IBM-GLOBAL-Appspprt-Fin-Non-Critical MES DRP iSeries,IBM-GLOBAL-AppSpprt-AN Spain Veeva Informatica Integration,IBM-GLOBAL-Appspprt-Fin-Critical Microsoft COTS,IBM-GLOBAL-AppSpprt-Commercial AP41,IBM-LATAM-AppSpprt-Finance BPCS Non Critical App Support,IBM-APAC-AppSpprt-Non-Critical Application Support,IBM-GLOBAL-AppSpprt-TCGM COGNOS Critical App Support,IBM-GLOBAL-AppSpprt-Symphony Esker,IBM-GLOBAL-AppSpprt-Cadency Trintech,IBM-GLOBAL-AppSpprt Rosslyn GSI,IBM-GLOBAL-AppSpprt-SCM Staging App Support,IBM-GLOBAL-AppSpprt-Legacy Procure to Pay Solutions,IBM-GLOBAL-AppSpprt-Megapay,IBM-GLOBAL-AppSpprt-TCGM WEB Critical App Support,IBM-GLOBAL-AppSpprt-OneConcur,IBM-GLOBAL-AppSpprt-DPO Reporting,IBM-GLOBAL-AppSpprt-ECMS,IBM-GLOBAL-AppSpprt-Clockwise,IBM-AMER-AppSpprt-Time and Attendance,IBM-GLOBAL-AppSpprt-GA23-Cognos,IBM-GLOBAL-Appspprt-Comm-Non-Critical Salesforce Veeva Apps,IBM-LATAM-AppSpprt-Uruguay-Qflow App Support,IBM-GLOBAL-AppSpprt-EIMS EDW,IBM-GLOBAL-Appspprt-ERP-FoF App Support,IBM-GLOBAL-AppSpprt-AP41 ISSG Support,IBM-GLOBAL-AppSpprt-ALM PowerPlan,IBM-EMEA-AppSpprt-DE-Finance Non-Critical App Support,IBM-GLOBAL-AppSpprt-CORP-FTPServer Operations,IBM-GLOBAL-AppSpprt-EIMS Symphony BW,IBM-GLOBAL-AppSpprt-Hyperion SHAPE Technical,IBM-GLOBAL-Appspprt-Fin-Critical Cognos Planning Reporting ETL,IBM-GLOBAL-AppSpprt-EIMS Cognos,IBM-GLOBAL-AppSpprt-TCGM SQL Critical App Support,IBM-GLOBAL-AppSpprt-Legacy Financial Solutions,IBM-GLOBAL-AppSpprt-ADM CORA Non Critical Applications,IBM-EMEA-AppSpprt-DE-Commercial Critical App Support,IBM-GLOBAL-AppSpprt-Non Critical Legacy Financial Solutions,IBM-GLOBAL-AppSpprt-Non Critical Legacy Procure to Pay Solutions,IBM-AMER-AppSpprt-Corporate Transfer Pricing - WANDA,IBM-GLOBAL-AppSpprt-HFM Applications,IBM-GLOBAL-AppSpprt-AVD Hyperion Planning,IBM-EMEA-AppSpprt-PL-Critical Application Support,IBM-GLOBAL-AppSpprt-Critical Hyperion SHAPE,IBM-GLOBAL-AppSpprt-EIMS ETL,IBM-GLOBAL-Appspprt-Fin-Non-Critical Java WebTech SaaS,IBM-GLOBAL-AppSpprt-Esker MD,IBM-GLOBAL-AppSpprt-TMS,IBM-GLOBAL-AppSpprt-Spreadsheet Server Non Critical Support,IBM-AMER-AppSpprt-Treasury Solutions,IBM-GLOBAL-AppSpprt-EIMS SCR ETL CRITICAL APP SUPPORT"
        if selected=="Integration":
            assignment_group_params = "assignment_group.nameINIBM-GLOBAL-AppSpprt-RIVA Non-Critical App Support,IBM-GLOBAL-AppSpprt-ESB,IBM-GLOBAL-AppSpprt-EDI,IBM-GLOBAL-AppSpprt-Abbott-FileTransfer Operations,IBM-GLOBAL-AppSpprt-Operations Middleware"
        if selected=="Legacy ERP":
            assignment_group_params = "assignment_group.nameINIBM-EMEA-SysAccessAdmin-ES-Access Administration Non-Critical App Support,IBM-EMEA-AppSpprt-ME-Non Critical App Support,IBM-GLOBAL-Appspprt-ERP-Non-Critical Java WebTech SaaS,IBM-APAC-AppSpprt-Hong Kong-Gold,IBM-AMER-AppSpprt-APOC-Ottawa/Princeton- Non Critical ERP Applications,IBM-APAC-AppSpprt-Taiwan-Gold,IBM-GLOBAL-Appspprt-ERP-Non-Critical Content Mgmt,IBM-EMEA-AppSpprt-FR-Non-Critical Application Support,IBM-EMEA-AppSpprt-PT-Non-Critical App Support,IBM-EMEA-AppSpprt-KE-Non Critical App Support,IBM-GLOBAL-Appspprt-ERP-Non-Critical Microsoft COTS,IBM-EMEA-AppSpprt-DE-Supply Chain Non-Critical App Support,IBM-GLOBAL-Appspprt-ERP-Critical ADC Model N,IBM-EMEA-AppSpprt-DE-Supply Chain Critical App Support,IBM-APAC-AppSpprt-Korea-Gold,IBM-EMEA-AppSpprt-CH-Non-Critical Application Support,IBM-GLOBAL-Appspprt-ERP-Critical ADD Model N,IBM-GLOBAL-DBA-Model N ADD,IBM-GLOBAL-Appspprt-ERP-Critical Java WebTech SaaS,IBM-APAC-AppSpprt-ANZ-GOLD"
        if selected=="Manufacturing":
            assignment_group_params = "assignment_group.nameINIBM-GLOBAL-AppSpprt-DTM IT Support,IBM-GLOBAL-Appspprt-MPD-Non-Critical LIMS Empower Nugenesis,IBM-GLOBAL-AppSpprt iRCE,IBM-GLOBAL-Appspprt-MPD-Critical LIMS Empower Nugenesis,IBM-GLOBAL-Appspprt-MPD-FoF App Support,IBM-GLOBAL-Appspprt-MPD-Critical MES DRP iSeries,IBM-GLOBAL-AppSpprt-QAWO IT Support,IBM-GLOBAL-Appspprt-MPD-Critical Java WebTech SaaS,IBM-GLOBAL-AppSpprt-APOGEE,IBM-GLOBAL-AppSpprt-GES COGNOS Technical,IBM-GLOBAL-AppSpprt-Process Alarm,IBM-GLOBAL-AppSpprt-Maximo Infrastructure,IBM-GLOBAL-AppSpprt-ADMS Critical App Support,IBM-GLOBAL-AppSpprt-Middleware,IBM-GLOBAL-Appspprt-MPD-Non-Critical MES DRP iSeries,IBM-GLOBAL-Appspprt-MPD-Critical Cognos Planning Reporting ETL,IBM-GLOBAL-AppSpprt-GES Security,IBM-GLOBAL-AppSpprt-AN Non Critical WMS,IBM-GLOBAL-AppSpprt-AN MANU,IBM-GLOBAL-AppSpprt-ADD ATS LAB,IBM-GLOBAL-AppSpprt-REACH IS,IBM-GLOBAL-Appspprt-MPD-Non-Crtical LIMS Empower Nugenesis,IBM-GLOBAL-Appspprt-MPD-Non-Critical PLM,IBM-GLOBAL-Appspprt-MPD-Non-Critical Cognos Planning Reporting ETL,IBM-GLOBAL-Appspprt-MPD-Non-Critical Java WebTech SaaS,IBM-GLOBAL-Appspprt-Comm-Critical Adobe LivCycle,IBM-GLOBAL-Appspprt-MPD-Non-Critical Microsoft COTS,IBM-GLOBAL-Appspprt-MPD-Critical Content Mgmt,IBM-GLOBAL-AppSpprt-EHS Applications,IBM-GLOBAL-AppSpprt-AN WMS,IBM-GLOBAL-Appspprt-MPD-Critical Microsoft COTS,IBM-GLOBAL-AppSpprt-ADMS Non-Critical App Support,IBM-GLOBAL-AppSpprt-ADMS,IBM-GLOBAL-AppSpprt-SCM Web App Support,IBM-GLOBAL-AppSpprt-LC Site Operations Apps,IBM-EMEA-AppSpprt-GPO-Zwolle-Non Critical Business Applications,IBM-GLOBAL-AppSpprt-WERCS,IBM-GLOBAL-AppSpprt-Maximo Technical,IBM-AMER-AppSpprt-APOC-Ottawa/Princeton-ERP Applications"
        if selected=="Quality":
            assignment_group_params = "assignment_group.nameINIBM-GLOBAL-Appspprt-Qlty-Non-Critical Microsoft Product Dev & Approval,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support PLM,IBM-GLOBAL-Appspprt-Qlty-Critical App Support Documentum,IBM-GLOBAL-Appspprt-Qlty-FoF App Support,IBM-GLOBAL-Appspprt-Qlty-eMDO,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Information Management,IBM-GLOBAL-AppSpprt-Formulary Card Application Support,IBM-GLOBAL-Appspprt-Qlty-FoF Notes App Support,IBM-GLOBAL-Appspprt-Qlty-Critical App Support ADC iQ,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support -Net LATAM,IBM-GLOBAL-Appspprt-Qlty-Critical MD Discovery,IBM-GLOBAL-Appspprt-Qlty-FoF Microsoft App Support,IBM-GLOBAL-Appspprt-Qlty-Critical MD CinDART,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Product Dev & Approval,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Product Dev & Approval Veeva,IBM-GLOBAL-Appspprt-Qlty-Critical Microsoft App Support Viewpoint,IBM-GLOBAL-Appspprt-Qlty- Critical App Support Mfiles,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Product Dev & Approval -Net-4,Solution Tracking of Regulatory and Quality Systems - (SolTRAQs),IBM-GLOBAL-Appspprt-Qlty-Critical Other Ent Functions-Report & Analytics,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Microsoft Other Ent Functions,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Documentum Support,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support IQ,IBM-GLOBAL-Appspprt-Qlty-Critical Other Ent Functions ISOTrain,IBM-GLOBAL-Appspprt-Qlty-Critical App Support Smart Solve,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support Trackwise,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Microsoft App Support-LATAM,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Notes,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support Veeva,IBM-GLOBAL-Appspprt-Qlty-Critical App Support PLM,IBM-GLOBAL-Appspprt-Qlty-Critical App Support-Java,IBM-GLOBAL-Appspprt-Qlty-Critical App Support Trackwise,IBM-GLOBAL-Appspprt-Qlty-Critical Microsoft App Support,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support Java,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Microsoft App Support,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Information Management Documentum,IBM-GLOBAL-Appspprt-Qlty-Critical EPD Retention Samples,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support Documentum,IBM-GLOBAL-Appspprt-Qlty-Critical App Support- LIMS Apps,IBM-GLOBAL-Appspprt-Qlty-Critical Product Dev & Approval Report & Analytics,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Product Dev & Approval PLM"
        if selected=="SAP":
            assignment_group_params = "assignment_group.nameINIBM-GLOBAL-AppSpprt-Symphony OTC,IBM-GLOBAL-AppSpprt-CLM Non-Critical App Support,IBM-GLOBAL-AppSpprt-SAPHEGA PTP,IBM-GLOBAL-AppSpprt-SAPHEGA APO,IBM-GLOBAL-AppSpprt-EIMS Symphony Cognos,IBM-GLOBAL-AppSpprt-AVD SAP OTC,IBM-GLOBAL-AppSpprt-APO-SNP,IBM-GLOBAL-Appspprt-Comm-Non-Critical Microsoft COTS,IBM-GLOBAL-AppSpprt-AVD SAP RTR,MD-GLOBAL-AppSpprt-SAP-MD Services Sales L2,BTS-GLOBAL-AppSpprt-SAP-Catapult Record to Report (RTR) L2,IBM-GLOBAL-AppSpprt-AVD-SAP Security,IBM-GLOBAL-AppSpprt-APO-DP,IBM-GLOBAL-DBA-SAP BI,MD-GLOBAL-AppSpprt-SAP-MD Services Reporting & Analytics - HANA,IBM-GLOBAL-AppSpprt-Symphony Purchasing ECC,IBM-GLOBAL-AppSpprt-AVD SAP Basis,IBM-GLOBAL-AppSpprt-AES SAP,IBM-GLOBAL-AppSpprt-AVD SAP PTP,IBM-GLOBAL-AppSpprt-SAPHEGA RTR,IBM-GLOBAL-AppSpprt-SAP IBP Security,MD-GLOBAL-AppSpprt-SAP-MD Services Security,MD-GLOBAL-EntrprsInfoMgt-Reporting & Analytics - Business Objects,IBM-GLOBAL-AppSpprt-SAP-Catapult BW,IBM-GLOBAL-AppSpprt-Symphony Purchasing SRM,MD-GLOBAL-AppSpprt-SAP-MD Services BASIS,IBM-LATAM-AppSpprt-SAP Critical App Support,BTS-GLOBAL-AppSpprt-SAP-Catapult Business Warehouse L2,IBM-GLOBAL-AppSpprt-Symphony RTR,IBM-GLOBAL-AppSpprt-SAPHEGA BI,IBM-GLOBAL-AppSpprt-SAPHEGA SOLMAN,IBM-GLOBAL-AppSpprt-Serialization Support,IBM-GLOBAL-AppSpprt- Germany Payroll Authorization,IBM-GLOBAL-AppSpprt-SAP Ariba,BTS-GLOBAL-AppSpprt-SAP-Catapult Order To Cash (OTC) L2,IBM-GLOBAL-AppSpprt-SAP-Catapult BASIS,IBM-EMEA-AppSpprt-IE-Non-Critical Application Support,IBM-GLOBAL-AppSpprt-EPD SAP,IBM-GLOBAL-AppSpprt-SAP Security,IBM-GLOBAL-AppSpprt-SAP IBP,IBM-GLOBAL-AppSpprt-SAP DS Data Services,IBM-GLOBAL-DBA-SAP APO,IBM-EMEA-AppSpprt-PT-Critical App Support,IBM-GLOBAL-AppSpprt-Solution Manager Triage,IBM-GLOBAL-DBA-SAP AVD,MD-GLOBAL-AppSpprt-SAP-MD Services Logistics L2,MD-GLOBAL-AppSpprt-SAP-MD Services Operations L2,IBM-GLOBAL-AppSpprt-AVD SAP BW,IBM-GLOBAL-AppSpprt-SAP-ARDx BASIS,IBM-GLOBAL-AppSpprt-Symphony SCM,IBM-GLOBAL-AppSpprt-SAP-Catapult ErpDev,IBM-GLOBAL-AppSpprt-Symphony Vertex,IBM-GLOBAL-AppSpprt-APO,IBM-GLOBAL-AppSpprt-SAP BASIS,MD-GLOBAL-AppSpprt-SAP-MD Services Finance L2,IBM-GLOBAL-AppSpprt-SAP Security-ERP,BTS-GLOBAL-AppSpprt-SAP-Catapult Supply Chain Management (SCM) L2,MD-GLOBAL-AppSpprt-SAP-MD Services ERP-Dev,MD-GLOBAL-AppSpprt-SAP-MD Services PDT L2,IBM-GLOBAL-AppSpprt- Germany Payroll BASIS,IBM-GLOBAL-AppSpprt-Symphony ILM,IBM-GLOBAL-AppSpprt-SAPHEGA OTC,IBM-GLOBAL-AppSpprt-Symphony Payables ECC,IBM-GLOBAL-AppSpprt-SAP-Catapult Security,MD-GLOBAL-AppSpprt-SAP-MD Services Reporting & Analytics - Business Warehouse,IBM-GLOBAL-AppSpprt-SAPHEGA MANUFACTURING,IBM-GLOBAL-DBA-SAP Symphony,IBM-GLOBAL-AppSpprt-SAP P30 OTC,IBM-GLOBAL-AppSpprt-SAP P30 AE,IBM-GLOBAL-AppSpprt-SAPHEGA AUTHORIZATION,IBM-GLOBAL-AppSpprt-Symphony MDG,BTS-GLOBAL-AppSpprt-SAP-Catapult Procure to Pay (PTP) L2,MD-GLOBAL-EntrprsInfoMgt-Reporting & Analytics - Pulse,IBM-GLOBAL-AppSpprt-GRC Access Control,IBM-GLOBAL-AppSpprt-SAP P30 RTR,BTS-GLOBAL-AppSpprt-SAP-Catapult HR MiniMaster L2,MD-APAC-AppSpprt-SAP-MD Services China SAP Security,IBM-GLOBAL-AppSpprt-SAP P30 PTP"
        if priorityselected !="All":
            # st.write(priorityselected)
            priorityvalue = str(priorityselected)
            assignment_group_params = f"priority={priorityvalue}^{assignment_group_params}"
        data = api.get_incidents(start_date, end_date, assignment_group_params)
        df = pd.DataFrame(data) 
        st.write("Total Incidents: ",len(df)) 
        
        # Make sure the date columns are in datetime format
        df["opened_at"] = pd.to_datetime(df["opened_at"], errors="coerce")
        df["closed_at"] = pd.to_datetime(df["closed_at"], errors="coerce")

        # Extract year-month from the datetime
        df["opened_month"] = df["opened_at"].dt.to_period("M").astype(str)
        df["closed_month"] = df["closed_at"].dt.to_period("M").astype(str)

        # Count incidents opened and closed by month
        opened_counts = df["opened_month"].value_counts().sort_index().reset_index()
        opened_counts.columns = ["Month", "Opened"]

        closed_counts = df["closed_month"].value_counts().sort_index().reset_index()
        closed_counts.columns = ["Month", "Closed"]

        # Merge open/close counts
        combined = pd.merge(opened_counts, closed_counts, on="Month", how="outer").fillna(0)
        combined = combined.sort_values("Month")

        # Convert counts to integers
        combined["Opened"] = combined["Opened"].astype(int)
        combined["Closed"] = combined["Closed"].astype(int)

        # Melt for grouped bar chart
        long_df = pd.melt(combined, id_vars=["Month"], value_vars=["Opened", "Closed"],
                        var_name="Status", value_name="Count")

        # Plot with Plotly
        fig1 = px.bar(long_df, x="Month", y="Count", color="Status", barmode="group",
                    title="Incidents Opened and Closed per Month")
        
        st.plotly_chart(fig1, use_container_width=True)
        combined["Resolution Rate (%)"] = (combined["Closed"] / combined["Opened"]) * 100
        fig2 = px.line(
        combined,
        x="Month",
        y="Resolution Rate (%)",
        title="Monthly Incident Resolution Rate",
        markers=True)
        fig2.update_traces(line=dict(color="green", width=3))
        st.plotly_chart(fig2, use_container_width=True)
        category_counts = df["category"].value_counts().reset_index()
        category_counts.columns = ["Category", "Count"]

        fig3 = px.bar(category_counts, x="Category", y="Count", title="Incidents by Category",color_discrete_sequence=["#9EE6CF"])
        #fig.show()
        st.plotly_chart(fig3, use_container_width=True)
        st.write(df)
        st.download_button("Download Incidents", df.to_csv().encode(), "incidents.csv")

with tabs[1]:
    st.header("Service Requests")
    # if st.button("Load Service Requests"):
    #     col3,col4 = st.columns(2)
    # with col3:
    #     options = ["All", "ANI-LATAM", "BPCS", "Collaboration", "DBA", "Finance", "Integration", "Legacy ERP", "Manufacturing", "Quality", "SAP"]
    #     selected2 = st.selectbox("Choose an option: ", options, index=0)
    # with col4:
    #     priorityoptions = ["All", "1", "2", "3", "4"]
    #     priorityselected = st.selectbox("Select Priority: ", priorityoptions)
    # if st.button("Load Incidents"):        
    #     if selected2=="ANI-LATAM":
    #         assignment_group_params = "assignment_group.nameINANI-LATAM-AppSpprt-Nutritional Connection,ANI-LATAM-AppSpprt-LATAM Marketing Cloud,ANI-LATAM-AppSpprt-Pitcher Meteoro,ANI-LATAM-AppSpprt-LATAM Salesforce Service Cloud,ANI-LATAM-AppSpprt-LATAM Verify,ANI-LATAM-AppSpprt-Message Bird,ANI-LATAM-AppSpprt-Contigo Loyalty"
    #     if selected2=="BPCS":
    #         assignment_group_params = "assignment_group.nameINIBM-EMEA-AppSpprt-ME-Critical App Support,IBM-APAC-AppSpprt-BPCS-5.1,IBM-EMEA-AppSpprt-ES-Access Administration Critical App Support,IBM-LATAM-AppSpprt-Finance BPCS Critical App Support,IBM-APAC-AppSpprt-Indonesia-Gold,IBM-GLOBAL-AppSpprt-Thenon Admin Support,IBM-EMEA-AppSpprt-FR-Critical Application Support,IBM-EMEA-AppSpprt-BE-Critical Application Support,IBM-EMEA-AppSpprt-EG-Critical App Support,IBM-EMEA-AppSpprt-TR-Finance Critical App Support,IBM-EMEA-AppSpprt-SA-Critical App Support,IBM-EMEA-AppSpprt-TR-Finance Non-Critical App Support,IBM-EMEA-AppSpprt-GPO-Zwolle-Business Applications,IBM-EMEA-AppSpprt-ZA-Critical App Support,IBM-APAC-AppSpprt-Malaysia-Gold,IBM-EMEA-AppSpprt-NL-BPCS Zwolle Support,IBM-EMEA-AppSpprt-IT-Non-Critical Application Support,IBM-EMEA-AppSpprt-PL-Non Critical Application Support,IBM-APAC-AppSpprt-China-Gold,IBM-EMEA-AppSpprt-IT-Critical Application Support,IBM-EMEA-AppSpprt-ES-Maintenance Non-Critical App Support,IBM-APAC-AppSpprt-Vietnam-Gold,IBM-EMEA-AppSpprt-ES-Maintenance Critical App Support,IBM-APAC-AppSpprt-Philippines-Gold"
    #     if selected2=="Collaboration":
    #         assignment_group_params = "assignment_group.nameINIBM-GLOBAL-AppSpprt-ALM Services,IBM-GLOBAL-Appspprt-ColTech-Critical Commercial Digital,IBM-GLOBAL-Appspprt-ColTech-Critical IICS,IBM-GLOBAL-Appspprt-ColTech-Critical Intranet Websites,IBM-GLOBAL-Appspprt-ColTech-Critical Notes,IBM-GLOBAL-Appspprt-ColTech-Critical Other Ent Functions,IBM-GLOBAL-Appspprt-ColTech-Critical SharePoint,IBM-GLOBAL-Appspprt-ColTech-FoF App Support,IBM-GLOBAL-Appspprt-ColTech-FoF Intranet Websites,IBM-GLOBAL-Appspprt-ColTech-FoF Notes App Support,IBM-GLOBAL-Appspprt-ColTech-FoF Other Ent Functions App Support,IBM-GLOBAL-Appspprt-ColTech-FoF SharePoint,IBM-GLOBAL-Appspprt-ColTech-Intranet Websites,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Commercial,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Commercial Digital,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Commercial SFDC,IBM-GLOBAL-AppSpprt-ColTech-Non-Critical Content Mgmt,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Finance,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Human Resources,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Information Management,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Intranet Websites,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Manufacturing,IBM-GLOBAL-Appspprt-ColTech-Non-Critical MSPS Support,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Notes,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Other Ent Functions,IBM-GLOBAL-Appspprt-ColTech-Non-Critical PIM,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Salesforce Veeva Apps,IBM-GLOBAL-Appspprt-ColTech-Non-Critical SharePoint,IBM-GLOBAL-Appspprt-ColTech-Non-Critical Technology,IBM-Global-AppSpprt-MEDDEV-Non-Critical-WebApplications"
    #         # assignment_group_params = urllib.parse.quote(",".join(assignment_group_params))
    #     if selected2=="DBA":
    #         assignment_group_params = "assignment_group.nameINIBM-GLOBAL-DBA-MYSQL,IBM-GLOBAL-DBA-TLE AHD,IBM-GLOBAL-DBA-WWOps DBA Oracle,IBM-GLOBAL-DBA-CCI,IBM-GLOBAL-DBA-HR DB CHR,IBM-GLOBAL-DBA-CHAD Kronos,IBM-GLOBAL-DBA-ISTP Abbott,IBM-GLOBAL-DBA-Operations Oracle,IBM-GLOBAL-DBA-Informatica,IBM-GLOBAL-DBA-Enterprise DBA Operations Oracle,IBM-GLOBAL-DBA-Autosys,IBM-GLOBAL-DBA-QSDW,IBM-GLOBAL-DBA-ITSM GIS,IBM-GLOBAL-DBA-DCFL ANI,IBM-GLOBAL-DBA-SQL Server,IBM-GLOBAL-DBA-SAP MD DBA Oracle,IBM-GLOBAL-DBA-TIBCO GIS,IBM-GLOBAL-DBA-Shape,IBM-GLOBAL-DBA-GES MXES,IBM-GLOBAL-DBA-Supermaster,IBM-GLOBAL-DBA-SCMStaging ANI,IBM-GLOBAL-DBA-QC,IBM-GLOBAL-DBA-EDW,IBM-GLOBAL-DBA-TCGM,IBM-GLOBAL-DBA-ADD LIMS QIMS"
    #     if selected2=="Finance":
    #         assignment_group_params = "assignment_group.nameINIBM-GLOBAL-Appspprt-Fin-Non-Critical Salesforce Veeva Apps,IBM-AMER-AppSpprt-CA-JDE Critical App Support,IBM-GLOBAL-AppSpprt-HQ Financial Critical Applications,IBM-GLOBAL-AppSpprt-OLAP Cube,IBM-LATAM-AppSpprt-ADAM,IBM-GLOBAL-AppSpprt-QSDW Level 2,IBM-GLOBAL-Appspprt-Fin-Non-Critical Cognos Planning Reporting ETL,IBM-GLOBAL-AppSpprt-EIMS SCR COGNOS CRITICAL APP SUPPORT,IBM-LATAM-AppSpprt-Brazil-Symphony BoltOn App Support,IBM-GLOBAL-Appspprt-Fin-Critical MES DRP iSeries,IBM-GLOBAL-AppSpprt-CCI Application Engineering,IBM-GLOBAL-AppSpprt-XMS Financial Solutions,IBM-GLOBAL-AppSpprt-APT,IBM-GLOBAL-AppSpprt-EIMS SCR WEB CRITICAL APP SUPPORT,IBM-GLOBAL-Appspprt-Fin-Non-Critical Microsoft COTS,IBM-GLOBAL-AppSpprt-Critical GRC Access Control,IBM-GLOBAL-AppSpprt-AN FC-Finance and HR Support,IBM-GLOBAL-AppSpprt-OnBase OCR Brainware,IBM-GLOBAL-AppSpprt-Hyperion SHAPE,IBM-GLOBAL-Appspprt-Fin-Non-Critical MES DRP iSeries,IBM-GLOBAL-AppSpprt-AN Spain Veeva Informatica Integration,IBM-GLOBAL-Appspprt-Fin-Critical Microsoft COTS,IBM-GLOBAL-AppSpprt-Commercial AP41,IBM-LATAM-AppSpprt-Finance BPCS Non Critical App Support,IBM-APAC-AppSpprt-Non-Critical Application Support,IBM-GLOBAL-AppSpprt-TCGM COGNOS Critical App Support,IBM-GLOBAL-AppSpprt-Symphony Esker,IBM-GLOBAL-AppSpprt-Cadency Trintech,IBM-GLOBAL-AppSpprt Rosslyn GSI,IBM-GLOBAL-AppSpprt-SCM Staging App Support,IBM-GLOBAL-AppSpprt-Legacy Procure to Pay Solutions,IBM-GLOBAL-AppSpprt-Megapay,IBM-GLOBAL-AppSpprt-TCGM WEB Critical App Support,IBM-GLOBAL-AppSpprt-OneConcur,IBM-GLOBAL-AppSpprt-DPO Reporting,IBM-GLOBAL-AppSpprt-ECMS,IBM-GLOBAL-AppSpprt-Clockwise,IBM-AMER-AppSpprt-Time and Attendance,IBM-GLOBAL-AppSpprt-GA23-Cognos,IBM-GLOBAL-Appspprt-Comm-Non-Critical Salesforce Veeva Apps,IBM-LATAM-AppSpprt-Uruguay-Qflow App Support,IBM-GLOBAL-AppSpprt-EIMS EDW,IBM-GLOBAL-Appspprt-ERP-FoF App Support,IBM-GLOBAL-AppSpprt-AP41 ISSG Support,IBM-GLOBAL-AppSpprt-ALM PowerPlan,IBM-EMEA-AppSpprt-DE-Finance Non-Critical App Support,IBM-GLOBAL-AppSpprt-CORP-FTPServer Operations,IBM-GLOBAL-AppSpprt-EIMS Symphony BW,IBM-GLOBAL-AppSpprt-Hyperion SHAPE Technical,IBM-GLOBAL-Appspprt-Fin-Critical Cognos Planning Reporting ETL,IBM-GLOBAL-AppSpprt-EIMS Cognos,IBM-GLOBAL-AppSpprt-TCGM SQL Critical App Support,IBM-GLOBAL-AppSpprt-Legacy Financial Solutions,IBM-GLOBAL-AppSpprt-ADM CORA Non Critical Applications,IBM-EMEA-AppSpprt-DE-Commercial Critical App Support,IBM-GLOBAL-AppSpprt-Non Critical Legacy Financial Solutions,IBM-GLOBAL-AppSpprt-Non Critical Legacy Procure to Pay Solutions,IBM-AMER-AppSpprt-Corporate Transfer Pricing - WANDA,IBM-GLOBAL-AppSpprt-HFM Applications,IBM-GLOBAL-AppSpprt-AVD Hyperion Planning,IBM-EMEA-AppSpprt-PL-Critical Application Support,IBM-GLOBAL-AppSpprt-Critical Hyperion SHAPE,IBM-GLOBAL-AppSpprt-EIMS ETL,IBM-GLOBAL-Appspprt-Fin-Non-Critical Java WebTech SaaS,IBM-GLOBAL-AppSpprt-Esker MD,IBM-GLOBAL-AppSpprt-TMS,IBM-GLOBAL-AppSpprt-Spreadsheet Server Non Critical Support,IBM-AMER-AppSpprt-Treasury Solutions,IBM-GLOBAL-AppSpprt-EIMS SCR ETL CRITICAL APP SUPPORT"
    #     if selected2=="Integration":
    #         assignment_group_params = "assignment_group.nameINIBM-GLOBAL-AppSpprt-RIVA Non-Critical App Support,IBM-GLOBAL-AppSpprt-ESB,IBM-GLOBAL-AppSpprt-EDI,IBM-GLOBAL-AppSpprt-Abbott-FileTransfer Operations,IBM-GLOBAL-AppSpprt-Operations Middleware"
    #     if selected2=="Legacy ERP":
    #         assignment_group_params = "assignment_group.nameINIBM-EMEA-SysAccessAdmin-ES-Access Administration Non-Critical App Support,IBM-EMEA-AppSpprt-ME-Non Critical App Support,IBM-GLOBAL-Appspprt-ERP-Non-Critical Java WebTech SaaS,IBM-APAC-AppSpprt-Hong Kong-Gold,IBM-AMER-AppSpprt-APOC-Ottawa/Princeton- Non Critical ERP Applications,IBM-APAC-AppSpprt-Taiwan-Gold,IBM-GLOBAL-Appspprt-ERP-Non-Critical Content Mgmt,IBM-EMEA-AppSpprt-FR-Non-Critical Application Support,IBM-EMEA-AppSpprt-PT-Non-Critical App Support,IBM-EMEA-AppSpprt-KE-Non Critical App Support,IBM-GLOBAL-Appspprt-ERP-Non-Critical Microsoft COTS,IBM-EMEA-AppSpprt-DE-Supply Chain Non-Critical App Support,IBM-GLOBAL-Appspprt-ERP-Critical ADC Model N,IBM-EMEA-AppSpprt-DE-Supply Chain Critical App Support,IBM-APAC-AppSpprt-Korea-Gold,IBM-EMEA-AppSpprt-CH-Non-Critical Application Support,IBM-GLOBAL-Appspprt-ERP-Critical ADD Model N,IBM-GLOBAL-DBA-Model N ADD,IBM-GLOBAL-Appspprt-ERP-Critical Java WebTech SaaS,IBM-APAC-AppSpprt-ANZ-GOLD"
    #     if selected2=="Manufacturing":
    #         assignment_group_params = "assignment_group.nameINIBM-GLOBAL-AppSpprt-DTM IT Support,IBM-GLOBAL-Appspprt-MPD-Non-Critical LIMS Empower Nugenesis,IBM-GLOBAL-AppSpprt iRCE,IBM-GLOBAL-Appspprt-MPD-Critical LIMS Empower Nugenesis,IBM-GLOBAL-Appspprt-MPD-FoF App Support,IBM-GLOBAL-Appspprt-MPD-Critical MES DRP iSeries,IBM-GLOBAL-AppSpprt-QAWO IT Support,IBM-GLOBAL-Appspprt-MPD-Critical Java WebTech SaaS,IBM-GLOBAL-AppSpprt-APOGEE,IBM-GLOBAL-AppSpprt-GES COGNOS Technical,IBM-GLOBAL-AppSpprt-Process Alarm,IBM-GLOBAL-AppSpprt-Maximo Infrastructure,IBM-GLOBAL-AppSpprt-ADMS Critical App Support,IBM-GLOBAL-AppSpprt-Middleware,IBM-GLOBAL-Appspprt-MPD-Non-Critical MES DRP iSeries,IBM-GLOBAL-Appspprt-MPD-Critical Cognos Planning Reporting ETL,IBM-GLOBAL-AppSpprt-GES Security,IBM-GLOBAL-AppSpprt-AN Non Critical WMS,IBM-GLOBAL-AppSpprt-AN MANU,IBM-GLOBAL-AppSpprt-ADD ATS LAB,IBM-GLOBAL-AppSpprt-REACH IS,IBM-GLOBAL-Appspprt-MPD-Non-Crtical LIMS Empower Nugenesis,IBM-GLOBAL-Appspprt-MPD-Non-Critical PLM,IBM-GLOBAL-Appspprt-MPD-Non-Critical Cognos Planning Reporting ETL,IBM-GLOBAL-Appspprt-MPD-Non-Critical Java WebTech SaaS,IBM-GLOBAL-Appspprt-Comm-Critical Adobe LivCycle,IBM-GLOBAL-Appspprt-MPD-Non-Critical Microsoft COTS,IBM-GLOBAL-Appspprt-MPD-Critical Content Mgmt,IBM-GLOBAL-AppSpprt-EHS Applications,IBM-GLOBAL-AppSpprt-AN WMS,IBM-GLOBAL-Appspprt-MPD-Critical Microsoft COTS,IBM-GLOBAL-AppSpprt-ADMS Non-Critical App Support,IBM-GLOBAL-AppSpprt-ADMS,IBM-GLOBAL-AppSpprt-SCM Web App Support,IBM-GLOBAL-AppSpprt-LC Site Operations Apps,IBM-EMEA-AppSpprt-GPO-Zwolle-Non Critical Business Applications,IBM-GLOBAL-AppSpprt-WERCS,IBM-GLOBAL-AppSpprt-Maximo Technical,IBM-AMER-AppSpprt-APOC-Ottawa/Princeton-ERP Applications"
    #     if selected2=="Quality":
    #         assignment_group_params = "assignment_group.nameINIBM-GLOBAL-Appspprt-Qlty-Non-Critical Microsoft Product Dev & Approval,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support PLM,IBM-GLOBAL-Appspprt-Qlty-Critical App Support Documentum,IBM-GLOBAL-Appspprt-Qlty-FoF App Support,IBM-GLOBAL-Appspprt-Qlty-eMDO,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Information Management,IBM-GLOBAL-AppSpprt-Formulary Card Application Support,IBM-GLOBAL-Appspprt-Qlty-FoF Notes App Support,IBM-GLOBAL-Appspprt-Qlty-Critical App Support ADC iQ,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support -Net LATAM,IBM-GLOBAL-Appspprt-Qlty-Critical MD Discovery,IBM-GLOBAL-Appspprt-Qlty-FoF Microsoft App Support,IBM-GLOBAL-Appspprt-Qlty-Critical MD CinDART,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Product Dev & Approval,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Product Dev & Approval Veeva,IBM-GLOBAL-Appspprt-Qlty-Critical Microsoft App Support Viewpoint,IBM-GLOBAL-Appspprt-Qlty- Critical App Support Mfiles,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Product Dev & Approval -Net-4,Solution Tracking of Regulatory and Quality Systems - (SolTRAQs),IBM-GLOBAL-Appspprt-Qlty-Critical Other Ent Functions-Report & Analytics,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Microsoft Other Ent Functions,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Documentum Support,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support IQ,IBM-GLOBAL-Appspprt-Qlty-Critical Other Ent Functions ISOTrain,IBM-GLOBAL-Appspprt-Qlty-Critical App Support Smart Solve,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support Trackwise,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Microsoft App Support-LATAM,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Notes,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support Veeva,IBM-GLOBAL-Appspprt-Qlty-Critical App Support PLM,IBM-GLOBAL-Appspprt-Qlty-Critical App Support-Java,IBM-GLOBAL-Appspprt-Qlty-Critical App Support Trackwise,IBM-GLOBAL-Appspprt-Qlty-Critical Microsoft App Support,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support Java,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Microsoft App Support,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Information Management Documentum,IBM-GLOBAL-Appspprt-Qlty-Critical EPD Retention Samples,IBM-GLOBAL-Appspprt-Qlty-Non-Critical App Support Documentum,IBM-GLOBAL-Appspprt-Qlty-Critical App Support- LIMS Apps,IBM-GLOBAL-Appspprt-Qlty-Critical Product Dev & Approval Report & Analytics,IBM-GLOBAL-Appspprt-Qlty-Non-Critical Product Dev & Approval PLM"
    #     if selected2=="SAP":
    #         assignment_group_params = "assignment_group.nameINIBM-GLOBAL-AppSpprt-Symphony OTC,IBM-GLOBAL-AppSpprt-CLM Non-Critical App Support,IBM-GLOBAL-AppSpprt-SAPHEGA PTP,IBM-GLOBAL-AppSpprt-SAPHEGA APO,IBM-GLOBAL-AppSpprt-EIMS Symphony Cognos,IBM-GLOBAL-AppSpprt-AVD SAP OTC,IBM-GLOBAL-AppSpprt-APO-SNP,IBM-GLOBAL-Appspprt-Comm-Non-Critical Microsoft COTS,IBM-GLOBAL-AppSpprt-AVD SAP RTR,MD-GLOBAL-AppSpprt-SAP-MD Services Sales L2,BTS-GLOBAL-AppSpprt-SAP-Catapult Record to Report (RTR) L2,IBM-GLOBAL-AppSpprt-AVD-SAP Security,IBM-GLOBAL-AppSpprt-APO-DP,IBM-GLOBAL-DBA-SAP BI,MD-GLOBAL-AppSpprt-SAP-MD Services Reporting & Analytics - HANA,IBM-GLOBAL-AppSpprt-Symphony Purchasing ECC,IBM-GLOBAL-AppSpprt-AVD SAP Basis,IBM-GLOBAL-AppSpprt-AES SAP,IBM-GLOBAL-AppSpprt-AVD SAP PTP,IBM-GLOBAL-AppSpprt-SAPHEGA RTR,IBM-GLOBAL-AppSpprt-SAP IBP Security,MD-GLOBAL-AppSpprt-SAP-MD Services Security,MD-GLOBAL-EntrprsInfoMgt-Reporting & Analytics - Business Objects,IBM-GLOBAL-AppSpprt-SAP-Catapult BW,IBM-GLOBAL-AppSpprt-Symphony Purchasing SRM,MD-GLOBAL-AppSpprt-SAP-MD Services BASIS,IBM-LATAM-AppSpprt-SAP Critical App Support,BTS-GLOBAL-AppSpprt-SAP-Catapult Business Warehouse L2,IBM-GLOBAL-AppSpprt-Symphony RTR,IBM-GLOBAL-AppSpprt-SAPHEGA BI,IBM-GLOBAL-AppSpprt-SAPHEGA SOLMAN,IBM-GLOBAL-AppSpprt-Serialization Support,IBM-GLOBAL-AppSpprt- Germany Payroll Authorization,IBM-GLOBAL-AppSpprt-SAP Ariba,BTS-GLOBAL-AppSpprt-SAP-Catapult Order To Cash (OTC) L2,IBM-GLOBAL-AppSpprt-SAP-Catapult BASIS,IBM-EMEA-AppSpprt-IE-Non-Critical Application Support,IBM-GLOBAL-AppSpprt-EPD SAP,IBM-GLOBAL-AppSpprt-SAP Security,IBM-GLOBAL-AppSpprt-SAP IBP,IBM-GLOBAL-AppSpprt-SAP DS Data Services,IBM-GLOBAL-DBA-SAP APO,IBM-EMEA-AppSpprt-PT-Critical App Support,IBM-GLOBAL-AppSpprt-Solution Manager Triage,IBM-GLOBAL-DBA-SAP AVD,MD-GLOBAL-AppSpprt-SAP-MD Services Logistics L2,MD-GLOBAL-AppSpprt-SAP-MD Services Operations L2,IBM-GLOBAL-AppSpprt-AVD SAP BW,IBM-GLOBAL-AppSpprt-SAP-ARDx BASIS,IBM-GLOBAL-AppSpprt-Symphony SCM,IBM-GLOBAL-AppSpprt-SAP-Catapult ErpDev,IBM-GLOBAL-AppSpprt-Symphony Vertex,IBM-GLOBAL-AppSpprt-APO,IBM-GLOBAL-AppSpprt-SAP BASIS,MD-GLOBAL-AppSpprt-SAP-MD Services Finance L2,IBM-GLOBAL-AppSpprt-SAP Security-ERP,BTS-GLOBAL-AppSpprt-SAP-Catapult Supply Chain Management (SCM) L2,MD-GLOBAL-AppSpprt-SAP-MD Services ERP-Dev,MD-GLOBAL-AppSpprt-SAP-MD Services PDT L2,IBM-GLOBAL-AppSpprt- Germany Payroll BASIS,IBM-GLOBAL-AppSpprt-Symphony ILM,IBM-GLOBAL-AppSpprt-SAPHEGA OTC,IBM-GLOBAL-AppSpprt-Symphony Payables ECC,IBM-GLOBAL-AppSpprt-SAP-Catapult Security,MD-GLOBAL-AppSpprt-SAP-MD Services Reporting & Analytics - Business Warehouse,IBM-GLOBAL-AppSpprt-SAPHEGA MANUFACTURING,IBM-GLOBAL-DBA-SAP Symphony,IBM-GLOBAL-AppSpprt-SAP P30 OTC,IBM-GLOBAL-AppSpprt-SAP P30 AE,IBM-GLOBAL-AppSpprt-SAPHEGA AUTHORIZATION,IBM-GLOBAL-AppSpprt-Symphony MDG,BTS-GLOBAL-AppSpprt-SAP-Catapult Procure to Pay (PTP) L2,MD-GLOBAL-EntrprsInfoMgt-Reporting & Analytics - Pulse,IBM-GLOBAL-AppSpprt-GRC Access Control,IBM-GLOBAL-AppSpprt-SAP P30 RTR,BTS-GLOBAL-AppSpprt-SAP-Catapult HR MiniMaster L2,MD-APAC-AppSpprt-SAP-MD Services China SAP Security,IBM-GLOBAL-AppSpprt-SAP P30 PTP"
    #     if priorityselected !="All":
    #         # st.write(priorityselected)
    #         priorityvalue = str(priorityselected)
    #         assignment_group_params = f"priority={priorityvalue}^{assignment_group_params}"
    #     data = api.get_service_requests(start_date, end_date, assignment_group_params)
    #     df = pd.DataFrame(data)
    #     st.write("Total Requests: ",len(df)) 
        
    #     # Make sure the date columns are in datetime format
    #     df["opened_at"] = pd.to_datetime(df["opened_at"], errors="coerce")
    #     df["closed_at"] = pd.to_datetime(df["closed_at"], errors="coerce")

    #     # Extract year-month from the datetime
    #     df["opened_month"] = df["opened_at"].dt.to_period("M").astype(str)
    #     df["closed_month"] = df["closed_at"].dt.to_period("M").astype(str)

    #     # Count incidents opened and closed by month
    #     opened_counts = df["opened_month"].value_counts().sort_index().reset_index()
    #     opened_counts.columns = ["Month", "Opened"]

    #     closed_counts = df["closed_month"].value_counts().sort_index().reset_index()
    #     closed_counts.columns = ["Month", "Closed"]

    #     # Merge open/close counts
    #     combined = pd.merge(opened_counts, closed_counts, on="Month", how="outer").fillna(0)
    #     combined = combined.sort_values("Month")

    #     # Convert counts to integers
    #     combined["Opened"] = combined["Opened"].astype(int)
    #     combined["Closed"] = combined["Closed"].astype(int)

    #     # Melt for grouped bar chart
    #     long_df = pd.melt(combined, id_vars=["Month"], value_vars=["Opened", "Closed"],
    #                     var_name="Status", value_name="Count")

    #     # Plot with Plotly
    #     fig1 = px.bar(long_df, x="Month", y="Count", color="Status", barmode="group",
    #                 title="Requests Opened and Closed per Month")
        
    #     st.plotly_chart(fig1, use_container_width=True)
    #     combined["Resolution Rate (%)"] = (combined["Closed"] / combined["Opened"]) * 100
    #     fig2 = px.line(
    #     combined,
    #     x="Month",
    #     y="Resolution Rate (%)",
    #     title="Monthly Requests Resolution Rate",
    #     markers=True)
    #     fig2.update_traces(line=dict(color="green", width=3))
    #     st.plotly_chart(fig2, use_container_width=True)
    #     category_counts = df["category"].value_counts().reset_index()
    #     category_counts.columns = ["Category", "Count"]

    #     fig3 = px.bar(category_counts, x="Category", y="Count", title="Requests by Category",color_discrete_sequence=["#9EE6CF"])
    #     #fig.show()
    #     st.plotly_chart(fig3, use_container_width=True)
    #     st.write(df)
    #     st.download_button("Download Requests", df.to_csv().encode(), "requests.csv")

with tabs[2]:
    st.header("Problems")
    if st.button("Load Problems"):
        data = api.get_problems(start_date.isoformat(), end_date.isoformat())
        df = pd.DataFrame(data)
        st.write(df)
        st.download_button("Download Problems", df.to_csv().encode(), "problems.csv")

with tabs[3]:
    st.header("SLA Details")
    if st.button("Load SLAs"):
        data = api.get_slas()
        df = pd.DataFrame(data)
        st.write(df)
        st.download_button("Download SLAs", df.to_csv().encode(), "slas.csv")

with tabs[4]:
    st.header("Assignment Groups")
    if st.button("Load Assignment Groups"):
        data = api.get_assignment_groups()
        df = pd.DataFrame(data)
        st.write(df)
        st.download_button("Download Groups", df.to_csv().encode(), "assignment_groups.csv")

with tabs[5]:
    st.header("Business Applications")
    if st.button("Load Business Applications"):
        data = api.get_business_apps()
        df = pd.DataFrame(data)
        st.write(df)
        st.download_button("Download Apps", df.to_csv().encode(), "business_apps.csv")