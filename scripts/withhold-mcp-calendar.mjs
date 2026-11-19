import { withholdManagementCalendar } from "./withhold-management-calendar.mjs";

export function withholdMcpCalendar(document) {
  withholdManagementCalendar(document);
  for (const path of Object.keys(document.paths)) {
    if (/^\/mailbox\/(calendars|calendar-events)(\/|$)/.test(path)) delete document.paths[path];
  }
  for (const name of Object.keys(document.components.schemas)) {
    if (/calendar/i.test(name)) delete document.components.schemas[name];
  }
  const scopes = document.components.securitySchemes.oauth2.flows.authorizationCode.scopes;
  delete scopes["calendar.read"];
  delete scopes["calendar.write"];
}
