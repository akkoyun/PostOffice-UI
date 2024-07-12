# Setup Root Path
import sys
sys.path.append('/home/postoffice/PostOffice/src')

# Import Packages
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, JSON, Index, UniqueConstraint, func
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from Setup.Database import Base

# [A] Model Database Model
class Model(Base):

	# Define Table Name
	__tablename__ = "Model"

	# Define Columns
	Model_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Model_Name = Column(String(100), nullable=False, unique=True)
	Model_Description = Column(String(255), nullable=True, server_default="No description")
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	devices = relationship("Device", back_populates="model")
	modems = relationship("Modem", back_populates="model")

# [B] Manufacturer Database Model
class Manufacturer(Base):

	# Define Table Name
	__tablename__ = "Manufacturer"

	# Define Columns
	Manufacturer_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Manufacturer_Name = Column(String(100), nullable=False, unique=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	devices = relationship("Device", back_populates="manufacturer")
	modems = relationship("Modem", back_populates="manufacturer")

# [C] Modem Database Model
class Modem(Base):

	# Define Table Name
	__tablename__ = "Modem"

	# Define Columns
	IMEI = Column(String(20), primary_key=True, unique=True, nullable=False)
	Model_ID = Column(Integer, ForeignKey("Model.Model_ID", ondelete="CASCADE"), nullable=False)
	Manufacturer_ID = Column(Integer, ForeignKey("Manufacturer.Manufacturer_ID", ondelete="CASCADE"), nullable=False)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	model = relationship("Model", back_populates="modems")
	manufacturer = relationship("Manufacturer", back_populates="modems")
	devices = relationship("Device", back_populates="modem")

# [D] GSM_Operator Database Model
class GSM_Operator(Base):

	# Define Table Name
	__tablename__ = "GSM_Operator"

	# Define Columns
	Operator_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	MCC_ID = Column(Integer, nullable=False)
	MCC_ISO = Column(String(20), nullable=False)
	MCC_Country_Name = Column(String(100), nullable=False)
	MCC_Country_Code = Column(Integer, nullable=True)
	MCC_Country_Flag_Image_URL = Column(String(255), nullable=True)
	MNC_ID = Column(Integer, nullable=False)
	MNC_Brand_Name = Column(String(100), nullable=False)
	MNC_Operator_Name = Column(String(100), nullable=False)
	MNC_Operator_Image_URL = Column(String(255), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	sims = relationship("SIM", back_populates="operator")

	# Define Table Arguments
	__table_args__ = (
		UniqueConstraint('MCC_ID', 'MNC_ID', name='uix_mcc_mnc'),
		Index('idx_mcc_id', 'MCC_ID'),
		Index('idx_mnc_id', 'MNC_ID'),
		Index('idx_mcc_iso', 'MCC_ISO'),
		Index('idx_mnc_operator_name', 'MNC_Operator_Name'),
	)

# [E] SIM Database Model
class SIM(Base):

	# Define Table Name
	__tablename__ = "SIM"

	# Define Columns
	SIM_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	ICCID = Column(String(25), unique=True, nullable=False)
	Operator_ID = Column(Integer, ForeignKey("GSM_Operator.Operator_ID", ondelete="CASCADE"), nullable=False)
	GSM_Number = Column(String(15), nullable=True)
	Status = Column(Boolean, nullable=False, server_default="1")
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	streams = relationship("Stream", back_populates="sim")
	operator = relationship("GSM_Operator", back_populates="sims")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_iccid', 'ICCID'),
		Index('idx_operator_id', 'Operator_ID'),
		Index('idx_gsm_number', 'GSM_Number'),
	)

# [F] Version Database Model
class Version(Base):

	# Define Table Name
	__tablename__ = "Version"

	# Define Columns
	Version_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Firmware = Column(String(20), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	devices = relationship("Device", back_populates="version")
	firmwares = relationship("Firmware", back_populates="version")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_firmware', 'Firmware'),
	)

# [G] Status Database Model
class Status(Base):

	# Define Table Name
	__tablename__ = "Status"

	# Define Columns
	Status_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Description = Column(String(255), nullable=False, unique=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	devices = relationship("Device", back_populates="status")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_status_description', 'Description'),
	)

# [H] Device Database Model
class Device(Base):

	# Define Table Name
	__tablename__ = "Device"

	# Define Columns
	Device_ID = Column(String(21), primary_key=True, unique=True, nullable=False)
	Status_ID = Column(Integer, ForeignKey("Status.Status_ID"), nullable=False)
	Version_ID = Column(Integer, ForeignKey("Version.Version_ID"), nullable=False)
	Project_ID = Column(Integer, ForeignKey("Project.Project_ID"), nullable=True)
	Model_ID = Column(Integer, ForeignKey("Model.Model_ID"), nullable=False)
	Manufacturer_ID = Column(Integer, ForeignKey("Manufacturer.Manufacturer_ID"), nullable=False)
	IMEI = Column(String(16), ForeignKey("Modem.IMEI"), nullable=False)
	Device_Name = Column(String(100), nullable=True)
	Last_Connection_IP = Column(String(15), nullable=True)
	Last_Connection_Time = Column(TIMESTAMP(timezone=True), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())
	Description = Column(String(255), nullable=True)

	# Define Relationships
	streams = relationship("Stream", back_populates="device")
	status = relationship("Status", back_populates="devices")
	version = relationship("Version", back_populates="devices")
	project = relationship("Project", back_populates="devices")
	model = relationship("Model", back_populates="devices")
	manufacturer = relationship("Manufacturer", back_populates="devices")
	modem = relationship("Modem", back_populates="devices")
	calibrations = relationship("Calibration", back_populates="device")
	chain = relationship("Rule_Chain", back_populates="devices")


	# Define Table Arguments
	__table_args__ = (
		Index('idx_device_id', 'Device_ID'),
		Index('idx_model_id', 'Model_ID'),
		Index('idx_manufacturer_id', 'Manufacturer_ID'),
		Index('idx_status_id', 'Status_ID'),
		Index('idx_device_version_id', 'Version_ID'),
		Index('idx_project_id', 'Project_ID'),
	)

# Project Database Model
class Project(Base):

	# Define Table Name
	__tablename__ = "Project"

	# Define Columns
	Project_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Project_Name = Column(String(100), nullable=False, unique=True)
	Project_Description = Column(String(255), nullable=True)
	Status = Column(Boolean, nullable=False, server_default="1")
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	devices = relationship("Device", back_populates="project")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_project_name', 'Project_Name'),
	)

# [O] Data_Segment Database Model
class Data_Segment(Base):

	# Define Table Name
	__tablename__ = "Data_Segment"

	# Define Columns
	Segment_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Segment_Name = Column(String(100), nullable=False, unique=True)
	Description = Column(String(255), nullable=False)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Relationship with Variable
	variables = relationship("Variable", back_populates="segment")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_segment_name', 'Segment_Name'),
		Index('idx_segment_description', 'Description'),
	)

# [N] Variable Database Model
class Variable(Base):

	# Define Table Name
	__tablename__ = "Variable"

	# Define Columns
	Variable_ID = Column(String(30), primary_key=True, unique=True, nullable=False)
	Variable_Description = Column(String(255), nullable=False)
	Variable_Unit = Column(String(10), nullable=True)
	Variable_Min_Value = Column(Float, nullable=True)
	Variable_Max_Value = Column(Float, nullable=True)
	Segment_ID = Column(Integer, ForeignKey("Data_Segment.Segment_ID"), nullable=False)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	segment = relationship("Data_Segment", back_populates="variables")
	measurements = relationship("Measurement", back_populates="variable")
	calibrations = relationship("Calibration", back_populates="variable")
	chain = relationship("Rule_Chain", back_populates="variables")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_variable_id', 'Variable_ID'),
		Index('idx_segment_id', 'Segment_ID'),
	)

# [L] Measurement Database Model
class Measurement(Base):

	# Define Table Name
	__tablename__ = "Measurement"

	# Define Columns
	Measurement_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Stream_ID = Column(Integer, ForeignKey("Stream.Stream_ID", ondelete="CASCADE"), nullable=False)
	Variable_ID = Column(String(30), ForeignKey("Variable.Variable_ID", ondelete="CASCADE"), nullable=False)
	Measurement_Value = Column(Float, nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

	# Define Relationships
	stream = relationship("Stream", back_populates="measurements")
	variable = relationship("Variable", back_populates="measurements")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_stream_variable', 'Stream_ID', 'Variable_ID'),
		Index('idx_measurement_value', 'Measurement_Value'),
	)

# [J] Stream Database Model
class Stream(Base):

	# Define Table Name
	__tablename__ = "Stream"

	# Define Columns
	Stream_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(21), ForeignKey("Device.Device_ID", ondelete="CASCADE"), nullable=False)
	Command_ID = Column(Integer, ForeignKey("Command.Command_ID", ondelete="CASCADE"), nullable=True)
	SIM_ID = Column(Integer, ForeignKey("SIM.SIM_ID", ondelete="CASCADE"), nullable=False)
	IP_Address = Column(String(16), ForeignKey("Connection.IP_Address"), nullable=True)
	Size = Column(Integer, nullable=True)
	Device_Time = Column(TIMESTAMP(timezone=True), nullable=False)
	Stream_Time = Column(TIMESTAMP(timezone=True), nullable=False)

	# Define Relationships
	device = relationship("Device", back_populates="streams")
	sim = relationship("SIM", back_populates="streams")
	measurements = relationship("Measurement", back_populates="stream")
	command = relationship("Command", back_populates="streams")
	ip_address = relationship("Connection", back_populates="streams")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_stream_device_id', 'Device_ID'),
		Index('idx_stream_sim_id', 'SIM_ID'),
		Index('idx_stream_time', 'Stream_Time'),
		Index('idx_stream_ip_address', 'IP_Address'),
		Index('idx_device_time', 'Device_Time'),
	)

# Command Database Model
class Command(Base):

	# Define Table Name
	__tablename__ = "Command"

	# Define Columns
	Command_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Command = Column(String(30), nullable=False, unique=True)
	Description = Column(String(255), nullable=False)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	streams = relationship("Stream", back_populates="command")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_command', 'Command'),
	)

# Unknown_Data Database Model
class Unknown_Data(Base):

	# Define Table Name
	__tablename__ = "Unknown_Data"

	# Define Columns
	Data_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Client_IP = Column(String(16), nullable=True)
	RAW_Data = Column(String(1024), nullable=True)
	Size = Column(Integer, nullable=True)
	Stream_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

	# Define Table Arguments
	__table_args__ = (
		Index('idx_unknown_data_id', 'Data_ID'),
	)

# Calibration Database Model
class Calibration(Base):

	# Define Table Name
	__tablename__ = "Calibration"

	# Define Columns
	Calibration_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Device_ID = Column(String(21), ForeignKey("Device.Device_ID", ondelete="CASCADE"), nullable=False)
	Variable_ID = Column(String(30), ForeignKey("Variable.Variable_ID", ondelete="CASCADE"), nullable=False)
	Gain = Column(Float, nullable=False, server_default="1")
	Offset = Column(Float, nullable=False, server_default="0")
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	device = relationship("Device", back_populates="calibrations")
	variable = relationship("Variable", back_populates="calibrations")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_calibration_device_id', 'Device_ID'),
		Index('idx_calibration_variable_id', 'Variable_ID'),
		UniqueConstraint('Device_ID', 'Variable_ID', name='uix_device_variable'),
	)

# Firmware Database Model
class Firmware(Base):

	# Define Table Name
	__tablename__ = "Firmware"

	# Define Columns
	Firmware_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Version_ID = Column(Integer, ForeignKey("Version.Version_ID", ondelete="CASCADE"), nullable=False)
	File_Name = Column(String(255), nullable=True)
	Size = Column(Integer, nullable=True)
	Checksum = Column(String(64), nullable=True)
	Title = Column(String(100), nullable=True)
	URL = Column(String(255), nullable=True)
	Description = Column(String(255), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	version = relationship("Version", back_populates="firmwares")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_file_name', 'File_Name'),
		Index('idx_version_id', 'Version_ID'),
		Index('idx_create_time', 'Create_Time'),
		UniqueConstraint('File_Name', 'Version_ID', name='uix_file_version'),
	)

# Connection Database Model
class Connection(Base):

	# Define Table Name
	__tablename__ = "Connection"

	# Define Columns
	IP_Address = Column(String(16), nullable=False, primary_key=True, unique=True)
	IP_Pool = Column(Boolean, nullable=False, server_default="0")
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	streams = relationship("Stream", back_populates="ip_address")

# Rules Database Model
class Rules(Base):

	# Define Table Name
	__tablename__ = "Rules"

	# Define Columns
	Rule_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Rule_Name = Column(String(100), nullable=True)
	Rule_Description = Column(String(255), nullable=True)
	Rule_Action_ID = Column(Integer, nullable=True)
	Rule_Trigger_Count = Column(Integer, nullable=False, server_default="0")
	Rule_Status = Column(Boolean, nullable=False, server_default="1")
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	chain = relationship("Rule_Chain", back_populates="rules")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_rule_name', 'Rule_Name'),
		Index('idx_rule_description', 'Rule_Description')
	)

# Rule_Chain Database Model
class Rule_Chain(Base):

	# Define Table Name
	__tablename__ = "Rule_Chain"

	# Define Columns
	Rule_Chain_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Rule_ID = Column(Integer, ForeignKey("Rules.Rule_ID", ondelete="CASCADE"), nullable=False)
	Device_ID = Column(String(21), ForeignKey("Device.Device_ID", ondelete="CASCADE"), nullable=False)
	Variable_ID = Column(String(30), ForeignKey("Variable.Variable_ID", ondelete="CASCADE"), nullable=False)
	Rule_Operator = Column(String(10), nullable=False)
	Rule_Value = Column(Float, nullable=False)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Relationships
	rules = relationship("Rules", back_populates="chain")
	devices = relationship("Device", back_populates="chain")
	variables = relationship("Variable", back_populates="chain")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_rule_id', 'Rule_ID'),
		Index('idx_rulechain_device_id', 'Device_ID'),
		Index('idx_rulechain_variable_id', 'Variable_ID'),
		Index('idx_rulechain_time', 'Create_Time')
	)

# Discord Channel Database Model
class Discord(Base):

	# Define Table Name
	__tablename__ = "Discord"

	# Define Columns
	Discord_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Discord_Token = Column(String(255), nullable=False)
	Discord_Channel_ID = Column(String(255), nullable=False)
	Discord_Channel_Name = Column(String(100), nullable=False)
	Discord_Channel_Description = Column(String(255), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
	Update_Time = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())

	# Define Table Arguments
	__table_args__ = (
		Index('idx_discord_id', 'Discord_ID'),
		Index('idx_discord_token', 'Discord_Token'),
		Index('idx_discord_channel_id', 'Discord_Channel_ID'),
		Index('idx_discord_channel_name', 'Discord_Channel_Name')
	)

# Log_Level Database Model
class Log_Level(Base):

	# Define Table Name
	__tablename__ = "Log_Level"

	# Define Columns
	Log_Level_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Log_Level_Name = Column(String(20), nullable=False, unique=True)
	Log_Level_Description = Column(String(255), nullable=False)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

	# Define Relationships
	logs = relationship("Log", back_populates="level")
	
	# Define Table Arguments
	__table_args__ = (
		Index('idx_log_level_name', 'Log_Level_Name'),
		Index('idx_log_level_description', 'Log_Level_Description'),
	)

# Service Database Model
class Service(Base):

	# Define Table Name
	__tablename__ = "Service"

	# Define Columns
	Service_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Service_Name = Column(String(100), nullable=False, unique=True)
	Service_Description = Column(String(255), nullable=False)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

	# Define Relationships
	logs = relationship("Log", back_populates="service")
	
	# Define Table Arguments
	__table_args__ = (
		Index('idx_service_name', 'Service_Name'),
		Index('idx_service_description', 'Service_Description'),
	)

# Log Description Database Model
class Log_Description(Base):

	# Define Table Name
	__tablename__ = "Log_Description"

	# Define Columns
	Log_Description_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Log_Description = Column(String(255), nullable=False, unique=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

	# Define Relationships
	logs = relationship("Log", back_populates="description")
	
	# Define Table Arguments
	__table_args__ = (
		Index('idx_log_description', 'Log_Description'),
	)

# Log Database Model
class Log(Base):

	# Define Table Name
	__tablename__ = "Log"

	# Define Columns
	Log_ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	Log_Level_ID = Column(Integer, ForeignKey("Log_Level.Log_Level_ID"), nullable=False)
	Log_Description_ID = Column(Integer, ForeignKey("Log_Description.Log_Description_ID"), nullable=False)
	Service_ID = Column(Integer, ForeignKey("Service.Service_ID"), nullable=False)
	Device_ID = Column(String(21), nullable=True)
	Log_Message = Column(String(255), nullable=True)
	Create_Time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())

	# Define Relationships
	level = relationship("Log_Level", back_populates="logs")
	description = relationship("Log_Description", back_populates="logs")
	service = relationship("Service", back_populates="logs")

	# Define Table Arguments
	__table_args__ = (
		Index('idx_log_level_id', 'Log_Level_ID'),
		Index('idx_log_description_id', 'Log_Description_ID'),
		Index('idx_log_service_id', 'Service_ID'),
	)


