import re


def extract_alert_list_values(source_code):
    alert_list_values = []

    # Split the source code into lines
    lines = source_code.split('\n')

    # Regex pattern to find alert_list assignments
    alert_list_pattern = re.compile(r'alert_list\[(\d+)\]\s*=\s*alert_list\[(\d+)\]\s*\+\s*":_alert_hdl.._min_prio"')

    # Iterate through each line to find alert_list assignments
    for line in lines:
        line_stripped = line.strip()

        # Check for alert_list assignments
        match = alert_list_pattern.search(line_stripped)
        if match:
            source_index = match.group(2)
            value = f"alert_list[{source_index}] + \":_alert_hdl.._min_prio\""
            alert_list_values.append(value)

    return alert_list_values


def track_set_dp_names(source_code):
    set_dp_names_values = []

    # Split the source code into lines
    lines = source_code.split('\n')

    # Extract alert_list values
    alert_list_values = extract_alert_list_values(source_code)

    # Regex pattern to find dynAppend calls
    dynappend_pattern = re.compile(r'dynAppend\s*\(\s*set_dp_names\s*,\s*(alert_list\[\d+\])\s*\)')

    # Iterate through each line to find dynAppend calls
    for line in lines:
        line_stripped = line.strip()

        # Check for dynAppend calls to set_dp_names
        match = dynappend_pattern.search(line_stripped)
        if match:
            alert_list_var = match.group(1)
            set_dp_names_values.append(f"{alert_list_var} + \":_alert_hdl.._min_prio\"")

    return set_dp_names_values

# 사용 예시
source_code_example = """
for(int i = 1 ; i <= dynlen(child_list); i++)
{
    //1. Check alarm list of child DP
    alert_list = dpNames(child_list[i] + ".alert.*");

    if(dynlen(alert_list) == 0)
    {
        writeLog(g_script_name,"There is no DP alarm list. child DP = " + child_list[i] , LV_WARN);
        continue;
    }

    for(int k = 1 ; k <= dynlen(alert_list) ; k++)
        alert_list[k] = alert_list[k] + ":_alert_hdl.._min_prio";

    rs = dpGet(alert_list, min_prio);

    if(!rs)
    {
        writeLog(g_script_name,"set_alarm_unacitve() - dpGet Success, alert_list = " + alert_list + ", min_prio list = " + min_prio, LV_DBG2);

        //2. Check the alarm's min_prio value
        for(int j = 1 ; j <= dynlen(alert_list) ; j++)
        {
            if(dynlen(min_prio) == j)
                tmp_min_prio = min_prio[j];
            else
            {
                tmp_min_prio = -1;
                dpGet(alert_list[j], tmp_min_prio);
            }

            //3. The min_prio value is changed to +50 only when the alarm is disabled.
            if( tmp_min_prio == ACTIVE_MODE || tmp_min_prio == ACTIVE_PMMODE_MODE)
            {
                tmp_min_prio = tmp_min_prio + MIN_PRIO_VALUE;
                dynAppend(set_dp_names, alert_list[j]);
                dynAppend(set_values, tmp_min_prio);
                dpSet(alert_list[j], tmp_min_prio);
            }
        }
    }
    else
    {
        writeLog(g_script_name,"set_alarm_unacitve() - dpGet Error, alert_list = " + alert_list, LV_WARN);
        is_set_result = false;
        continue;
    }
}    
"""

# set_dp_names에 어떤 값이 들어있는지 확인
set_dp_names_values = track_set_dp_names(source_code_example)
print("Values in set_dp_names:", set_dp_names_values)
