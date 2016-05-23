from common import *

TITLE = 'Zenoss: ' # TODO: Fina a unique attribute of this page
locator = {'ipFilter': '#device_grid-filter-ipAddress-inputEl',
           'deviceRows': "#device_grid-body table .x-grid-row"}

@timed
@assertPage(TITLE)
def getEvents(user, sortedBy, ascending):
    result = ActionResult('getEvents')

    time.sleep(3) # pop-up

    navButtons = findMany(user.driver, '#deviceDetailNav-body table .x-grid-row')
    navButtons[1].click() # Click the Events button

    find(user.driver, "#device_events")

    event_rows = findMany(user.driver, "#device_events-body table .x-grid-row")
    events = []
    for el in event_rows:
        events.append({
            "resource": findIn(el, ".x-grid-cell-device").text,
            "class": findIn(el, ".x-grid-cell-eventClass").text,
            "summary": findIn(el, ".x-grid-cell-summary").text,
            "first_seen": findIn(el, ".x-grid-cell-firstTime").text,
            "last_seen": findIn(el, ".x-grid-cell-lastTime").text,
            "count": findIn(el, ".x-grid-cell-count").text,
        })

    result.putData('events', events)

    return result

@timed
def lookAtGraphs(user):
    result = ActionResult('lookAtGraphs')

    navBtns = findMany(user.driver, '#deviceDetailNav-body table .x-grid-row')

    for btn in navBtns:
        if btn.text == 'Graphs':
            btn.click() # Click the Graphs button

    # TODO: Wait until the graphs are loaded.

    user.think(3)

    return result

@timed
def lookAtComponentGraphs(user):
    result = ActionResult('lookAtComponentGraphs')

    # Parse component type texts
    navBtns = findMany(user.driver, '#deviceDetailNav-body table .x-grid-row')
    btnTexts = []
    comp = False
    for btn in navBtns:
        if btn.text == 'Graphs':
            comp = False
        if comp:
            btnTexts.append(btn.text)
        if btn.text == 'Components':
            comp = True

    # Iterate through component types and click each item in each type
    for text in btnTexts:
        navBtns = findMany(user.driver, '#deviceDetailNav-body table .x-grid-row')
        for btn in navBtns:
            if btn.text == text:
                btn.click()
                rows = findMany(user.driver, '#component_card-body table .x-grid-row')
                for row in rows:
                    # When it clicks through the rows in the Network Routes table,
                    # the link to interface is clicked if no-headless.
                    if btn.text.startswith('Network Routes'):
                        cols = findManyIn(row, '.x-grid-cell')
                        cols[3].click()
                    else:
                        row.click()

                    user.think(3) # TODO: How long would a user think before proceeding?
                break

    return result

def zoomIn(user, times):
    result = ActionResult('zoomIn')

    toolbarBtns = findMany(user.driver, '#device_graphs .x-btn')
    for _ in range(times):
        toolbarBtns[1].click()

    # TODO: Click the refresh btn.

    return result