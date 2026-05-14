const instance = "yewtu.be"

chrome.declarativeNetRequest.updateDynamicRules({
  removeRuleIds: [1, 2],
  addRules: [{
    id: 1,
    priority: 1,
    condition: {
      urlFilter: "||youtube.com",
      resourceTypes: ["main_frame"],
      excludedInitiatorDomains: [instance]
    },
    action: {
      type: "redirect",
      redirect: {
        transform: {scheme: "https", host: instance}
      }
    }
  },
  {
    id: 2,
    priority: 1,
    condition: {
      urlFilter: "||youtube.com/embed",
      resourceTypes: ["sub_frame"]
    },
    action: {
      type: "redirect",
      redirect: {
        transform: {scheme: "https", host: instance}
      }
    }
  }]
});
