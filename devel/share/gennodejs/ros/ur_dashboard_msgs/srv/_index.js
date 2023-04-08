
"use strict";

let GetProgramState = require('./GetProgramState.js')
let GetRobotMode = require('./GetRobotMode.js')
let AddToLog = require('./AddToLog.js')
let IsProgramRunning = require('./IsProgramRunning.js')
let RawRequest = require('./RawRequest.js')
let IsProgramSaved = require('./IsProgramSaved.js')
let GetSafetyMode = require('./GetSafetyMode.js')
let IsInRemoteControl = require('./IsInRemoteControl.js')
let Popup = require('./Popup.js')
let GetLoadedProgram = require('./GetLoadedProgram.js')
let Load = require('./Load.js')

module.exports = {
  GetProgramState: GetProgramState,
  GetRobotMode: GetRobotMode,
  AddToLog: AddToLog,
  IsProgramRunning: IsProgramRunning,
  RawRequest: RawRequest,
  IsProgramSaved: IsProgramSaved,
  GetSafetyMode: GetSafetyMode,
  IsInRemoteControl: IsInRemoteControl,
  Popup: Popup,
  GetLoadedProgram: GetLoadedProgram,
  Load: Load,
};
