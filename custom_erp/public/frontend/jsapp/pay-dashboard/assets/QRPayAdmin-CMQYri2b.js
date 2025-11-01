var __async = (__this, __arguments, generator) => {
  return new Promise((resolve, reject) => {
    var fulfilled = (value) => {
      try {
        step(generator.next(value));
      } catch (e) {
        reject(e);
      }
    };
    var rejected = (value) => {
      try {
        step(generator.throw(value));
      } catch (e) {
        reject(e);
      }
    };
    var step = (x) => x.done ? resolve(x.value) : Promise.resolve(x.value).then(fulfilled, rejected);
    step((generator = generator.apply(__this, __arguments)).next());
  });
};
import { g as ref, c as computed, k as onMounted, a as createElementBlock, b as createBaseVNode, z as createVNode, A as withCtx, L as unref, t as toDisplayString, F as Fragment, M as renderList, e as createCommentVNode, ad as createStaticVNode, aa as resolveComponent, o as openBlock, I as createTextVNode, B as withDirectives, al as vModelCheckbox, n as normalizeClass } from "./vendor-BMb8bgkN.js";
import { j as _export_sfc, c as createResource, l as call } from "./ui-Ca38NmEL.js";
import { s as session } from "./index-Bgu5Yqv3.js";
const _hoisted_1 = { class: "min-h-screen bg-gray-50" };
const _hoisted_2 = { class: "bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20" };
const _hoisted_3 = { class: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" };
const _hoisted_4 = { class: "flex justify-between items-center py-6" };
const _hoisted_5 = { class: "max-w-7xl mx-auto px-3 sm:px-4 lg:px-6 py-4 sm:py-8" };
const _hoisted_6 = { class: "bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8" };
const _hoisted_7 = { class: "flex flex-wrap gap-4" };
const _hoisted_8 = { class: "bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden" };
const _hoisted_9 = { class: "px-6 py-4 border-b border-gray-200" };
const _hoisted_10 = { class: "text-sm text-gray-600 mt-1" };
const _hoisted_11 = {
  key: 0,
  class: "p-8 text-center"
};
const _hoisted_12 = {
  key: 1,
  class: "p-8 text-center"
};
const _hoisted_13 = {
  key: 2,
  class: "overflow-x-auto"
};
const _hoisted_14 = { class: "min-w-full divide-y divide-gray-200" };
const _hoisted_15 = { class: "bg-gray-50" };
const _hoisted_16 = { class: "px-6 py-3 text-left" };
const _hoisted_17 = ["checked"];
const _hoisted_18 = { class: "bg-white divide-y divide-gray-200" };
const _hoisted_19 = { class: "px-6 py-4 whitespace-nowrap" };
const _hoisted_20 = ["value"];
const _hoisted_21 = { class: "px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900" };
const _hoisted_22 = { class: "px-6 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_23 = { class: "px-6 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_24 = { class: "px-6 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_25 = { class: "px-6 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_26 = { class: "px-6 py-4 whitespace-nowrap" };
const _hoisted_27 = { class: "px-6 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_28 = { class: "px-6 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_29 = {
  key: 0,
  class: "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
};
const _hoisted_30 = { class: "bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto" };
const _hoisted_31 = { class: "px-6 py-4" };
const _hoisted_32 = { class: "mb-4" };
const _hoisted_33 = { class: "flex items-center justify-between" };
const _hoisted_34 = { class: "text-sm text-gray-900" };
const _hoisted_35 = { class: "space-y-2 max-h-60 overflow-y-auto" };
const _hoisted_36 = { class: "text-sm font-medium" };
const _hoisted_37 = { class: "text-sm" };
const _hoisted_38 = { class: "px-6 py-4 border-t border-gray-200 flex justify-end" };
const _hoisted_39 = {
  key: 0,
  class: "fixed inset-0 z-50 overflow-y-auto",
  role: "dialog",
  "aria-modal": "true"
};
const _hoisted_40 = { class: "flex items-center justify-center min-h-screen px-4 text-center" };
const _hoisted_41 = { class: "inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-md sm:w-full" };
const _hoisted_42 = { class: "bg-gray-50 px-6 py-4 sm:flex sm:flex-row-reverse" };
const _sfc_main = {
  __name: "QRPayAdmin",
  setup(__props) {
    const transactions = ref([]);
    const selectedTransactions = ref([]);
    const loading = ref(false);
    const processing = ref(false);
    const showResults = ref(false);
    const processingResults = ref({ count: 0, results: [] });
    const showOfflineDialog = ref(false);
    const isOnline = ref(typeof navigator !== "undefined" ? navigator.onLine : true);
    const transactionResource = createResource({
      url: "frappe.client.get_list",
      params: {
        doctype: "Fonepay QR Transaction",
        fields: ["name", "prn", "creation", "customer", "sales_invoice", "amount", "status", "retries", "timeout_at"],
        filters: { processed: 0 },
        order_by: "creation asc",
        limit: 500
      },
      auto: false
    });
    const allSelected = computed(() => {
      return transactions.value.length > 0 && selectedTransactions.value.length === transactions.value.length;
    });
    const unprocessedCount = computed(() => {
      return transactions.value.length;
    });
    const loadTransactions = () => __async(this, null, function* () {
      loading.value = true;
      try {
        const res = yield transactionResource.fetch();
        transactions.value = res || [];
      } catch (error) {
        if (isNetworkError(error)) {
          handleOfflineError();
        } else {
          console.error("Error loading transactions:", error);
          alert("Failed to load transactions: " + error.message);
        }
      } finally {
        loading.value = false;
      }
    });
    const refreshData = () => {
      loadTransactions();
    };
    const toggleAll = () => {
      if (allSelected.value) {
        selectedTransactions.value = [];
      } else {
        selectedTransactions.value = transactions.value.map((t) => t.name);
      }
    };
    const processSelected = () => __async(this, null, function* () {
      if (selectedTransactions.value.length === 0) return;
      if (!isOnline.value) {
        handleOfflineError();
        processingResults.value = {
          count: 0,
          results: selectedTransactions.value.map((tx) => ({ tx, status: "NO INTERNET" }))
        };
        showResults.value = true;
        return;
      }
      processing.value = true;
      try {
        const res = yield call("custom_erp.custom_erp.api.fonepay.process_unprocessed_qrs", {
          tx_names: selectedTransactions.value.join(","),
          limit: selectedTransactions.value.length
        });
        if (res) {
          processingResults.value = res;
          showResults.value = true;
          selectedTransactions.value = [];
          yield loadTransactions();
        }
      } catch (error) {
        if (isNetworkError(error)) {
          handleOfflineError();
          processingResults.value = {
            count: 0,
            results: selectedTransactions.value.length ? selectedTransactions.value.map((tx) => ({ tx, status: "NO INTERNET" })) : [{ tx: "Selection", status: "NO INTERNET" }]
          };
          showResults.value = true;
        } else {
          console.error("Error processing transactions:", error);
          alert("Failed to process transactions: " + error.message);
        }
      } finally {
        processing.value = false;
      }
    });
    const processAll = () => __async(this, null, function* () {
      if (!isOnline.value) {
        handleOfflineError();
        processingResults.value = {
          count: 0,
          results: (transactions.value || []).map((t) => ({ tx: t.name, status: "NO INTERNET" }))
        };
        showResults.value = true;
        return;
      }
      processing.value = true;
      try {
        const res = yield call("custom_erp.custom_erp.api.fonepay.process_unprocessed_qrs", { limit: 500 });
        if (res) {
          processingResults.value = res;
          showResults.value = true;
          selectedTransactions.value = [];
          yield loadTransactions();
        }
      } catch (error) {
        if (isNetworkError(error)) {
          handleOfflineError();
          processingResults.value = {
            count: 0,
            results: [{ tx: "ALL", status: "NO INTERNET" }]
          };
          showResults.value = true;
        } else {
          console.error("Error processing all transactions:", error);
          alert("Failed to process all transactions: " + error.message);
        }
      } finally {
        processing.value = false;
      }
    });
    const exportSelected = () => {
      if (selectedTransactions.value.length === 0) return;
      const selectedData = transactions.value.filter((t) => selectedTransactions.value.includes(t.name));
      const csvData = [
        ["Name", "PRN", "Created", "Customer", "Invoice", "Amount", "Status", "Retries", "Timeout"],
        ...selectedData.map((t) => [
          t.name,
          t.prn || "",
          t.creation || "",
          t.customer || "",
          t.sales_invoice || "",
          t.amount || "",
          t.status || "",
          t.retries || 0,
          t.timeout_at || ""
        ])
      ];
      const csv = csvData.map(
        (row) => row.map((cell) => `"${(cell || "").toString().replace(/"/g, '""')}"`).join(",")
      ).join("\n");
      const blob = new Blob([csv], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "qrpay_transactions.csv";
      a.click();
      URL.revokeObjectURL(url);
    };
    const getStatusClass = (status) => {
      const classes = {
        "CREATED": "bg-blue-100 text-blue-800",
        "VERIFIED": "bg-yellow-100 text-yellow-800",
        "SCANNED": "bg-purple-100 text-purple-800",
        "PENDING": "bg-orange-100 text-orange-800",
        "SUCCESS": "bg-green-100 text-green-800",
        "FAILED": "bg-red-100 text-red-800"
      };
      return classes[status] || "bg-gray-100 text-gray-800";
    };
    const getResultClass = (status) => {
      if (status === "SUCCESS") return "bg-green-50 text-green-800";
      if (status === "FAILED") return "bg-red-50 text-red-800";
      if (status === "ERROR") return "bg-red-50 text-red-800";
      if (status === "NO INTERNET") return "bg-red-50 text-red-800";
      return "bg-gray-50 text-gray-800";
    };
    const formatDate = (dateString) => {
      if (!dateString) return "N/A";
      try {
        const date = new Date(dateString);
        return date.toLocaleDateString("en-IN", {
          year: "numeric",
          month: "short",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit"
        });
      } catch (e) {
        return dateString;
      }
    };
    const formatAmount = (amount) => {
      if (!amount && amount !== 0) return "0.00";
      return Number(amount).toLocaleString("en-IN", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    };
    const isNetworkError = (error) => {
      const msg = String(error && (error.message || error)).toLowerCase();
      if (!isOnline.value) return true;
      return msg.includes("network") || msg.includes("failed to fetch") || msg.includes("net::") || msg.includes("econn") || msg.includes("enotfound") || msg.includes("err_connection");
    };
    const handleOfflineError = (message = "No internet connection. Please check/connect to the internet and try again.") => {
      showOfflineDialog.value = true;
    };
    onMounted(() => {
      loadTransactions();
      try {
        window.addEventListener("online", () => {
          isOnline.value = true;
        });
        window.addEventListener("offline", () => {
          isOnline.value = false;
        });
      } catch (e) {
      }
    });
    return (_ctx, _cache) => {
      const _component_Button = resolveComponent("Button");
      return openBlock(), createElementBlock(Fragment, null, [
        createBaseVNode("div", _hoisted_1, [
          createBaseVNode("div", _hoisted_2, [
            createBaseVNode("div", _hoisted_3, [
              createBaseVNode("div", _hoisted_4, [
                _cache[6] || (_cache[6] = createBaseVNode("div", null, [
                  createBaseVNode("h1", { class: "text-2xl font-bold text-gray-900" }, "QRPay Admin"),
                  createBaseVNode("p", { class: "text-sm text-gray-600" }, "Manage unprocessed Fonepay transactions")
                ], -1)),
                createVNode(_component_Button, {
                  onClick: _cache[0] || (_cache[0] = ($event) => unref(session).logout.submit()),
                  theme: "gray",
                  variant: "outline"
                }, {
                  default: withCtx(() => _cache[5] || (_cache[5] = [
                    createTextVNode("Logout")
                  ])),
                  _: 1,
                  __: [5]
                })
              ])
            ])
          ]),
          createBaseVNode("div", _hoisted_5, [
            createBaseVNode("div", _hoisted_6, [
              createBaseVNode("div", _hoisted_7, [
                createVNode(_component_Button, {
                  onClick: processSelected,
                  loading: processing.value,
                  disabled: selectedTransactions.value.length === 0,
                  theme: "blue"
                }, {
                  default: withCtx(() => [
                    createTextVNode(" Process Selected (" + toDisplayString(selectedTransactions.value.length) + ") ", 1)
                  ]),
                  _: 1
                }, 8, ["loading", "disabled"]),
                createVNode(_component_Button, {
                  onClick: processAll,
                  loading: processing.value,
                  theme: "green"
                }, {
                  default: withCtx(() => [
                    createTextVNode(" Process All (" + toDisplayString(unprocessedCount.value) + ") ", 1)
                  ]),
                  _: 1
                }, 8, ["loading"]),
                createVNode(_component_Button, {
                  onClick: exportSelected,
                  disabled: selectedTransactions.value.length === 0,
                  theme: "gray",
                  variant: "outline"
                }, {
                  default: withCtx(() => _cache[7] || (_cache[7] = [
                    createTextVNode(" Export Selected CSV ")
                  ])),
                  _: 1,
                  __: [7]
                }, 8, ["disabled"]),
                createVNode(_component_Button, {
                  onClick: refreshData,
                  loading: loading.value,
                  theme: "gray",
                  variant: "outline"
                }, {
                  default: withCtx(() => _cache[8] || (_cache[8] = [
                    createTextVNode(" Refresh ")
                  ])),
                  _: 1,
                  __: [8]
                }, 8, ["loading"])
              ])
            ]),
            createBaseVNode("div", _hoisted_8, [
              createBaseVNode("div", _hoisted_9, [
                _cache[9] || (_cache[9] = createBaseVNode("h2", { class: "text-lg font-semibold text-gray-900" }, "Unprocessed Transactions", -1)),
                createBaseVNode("p", _hoisted_10, toDisplayString(transactions.value.length) + " transactions found", 1)
              ]),
              loading.value ? (openBlock(), createElementBlock("div", _hoisted_11, _cache[10] || (_cache[10] = [
                createBaseVNode("div", { class: "animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto" }, null, -1),
                createBaseVNode("p", { class: "mt-2 text-gray-600" }, "Loading transactions...", -1)
              ]))) : transactions.value.length === 0 ? (openBlock(), createElementBlock("div", _hoisted_12, _cache[11] || (_cache[11] = [
                createBaseVNode("div", { class: "text-gray-400 text-6xl mb-4" }, "📄", -1),
                createBaseVNode("p", { class: "text-gray-600" }, "No unprocessed transactions found", -1)
              ]))) : (openBlock(), createElementBlock("div", _hoisted_13, [
                createBaseVNode("table", _hoisted_14, [
                  createBaseVNode("thead", _hoisted_15, [
                    createBaseVNode("tr", null, [
                      createBaseVNode("th", _hoisted_16, [
                        createBaseVNode("input", {
                          type: "checkbox",
                          checked: allSelected.value,
                          onChange: toggleAll,
                          class: "rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        }, null, 40, _hoisted_17)
                      ]),
                      _cache[12] || (_cache[12] = createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " PRN ", -1)),
                      _cache[13] || (_cache[13] = createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Created ", -1)),
                      _cache[14] || (_cache[14] = createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Customer ", -1)),
                      _cache[15] || (_cache[15] = createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Invoice ", -1)),
                      _cache[16] || (_cache[16] = createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Amount ", -1)),
                      _cache[17] || (_cache[17] = createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Status ", -1)),
                      _cache[18] || (_cache[18] = createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Retries ", -1)),
                      _cache[19] || (_cache[19] = createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Timeout ", -1))
                    ])
                  ]),
                  createBaseVNode("tbody", _hoisted_18, [
                    (openBlock(true), createElementBlock(Fragment, null, renderList(transactions.value, (transaction) => {
                      return openBlock(), createElementBlock("tr", {
                        key: transaction.name,
                        class: "hover:bg-gray-50"
                      }, [
                        createBaseVNode("td", _hoisted_19, [
                          withDirectives(createBaseVNode("input", {
                            type: "checkbox",
                            value: transaction.name,
                            "onUpdate:modelValue": _cache[1] || (_cache[1] = ($event) => selectedTransactions.value = $event),
                            class: "rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          }, null, 8, _hoisted_20), [
                            [vModelCheckbox, selectedTransactions.value]
                          ])
                        ]),
                        createBaseVNode("td", _hoisted_21, toDisplayString(transaction.prn || "N/A"), 1),
                        createBaseVNode("td", _hoisted_22, toDisplayString(formatDate(transaction.creation)), 1),
                        createBaseVNode("td", _hoisted_23, toDisplayString(transaction.customer || "N/A"), 1),
                        createBaseVNode("td", _hoisted_24, toDisplayString(transaction.sales_invoice || "N/A"), 1),
                        createBaseVNode("td", _hoisted_25, " ₹" + toDisplayString(formatAmount(transaction.amount)), 1),
                        createBaseVNode("td", _hoisted_26, [
                          createBaseVNode("span", {
                            class: normalizeClass(["inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium", getStatusClass(transaction.status)])
                          }, toDisplayString(transaction.status || "N/A"), 3)
                        ]),
                        createBaseVNode("td", _hoisted_27, toDisplayString(transaction.retries || 0), 1),
                        createBaseVNode("td", _hoisted_28, toDisplayString(formatDate(transaction.timeout_at)), 1)
                      ]);
                    }), 128))
                  ])
                ])
              ]))
            ]),
            showResults.value ? (openBlock(), createElementBlock("div", _hoisted_29, [
              createBaseVNode("div", _hoisted_30, [
                _cache[22] || (_cache[22] = createBaseVNode("div", { class: "px-6 py-4 border-b border-gray-200" }, [
                  createBaseVNode("h3", { class: "text-lg font-medium text-gray-900" }, "Processing Results")
                ], -1)),
                createBaseVNode("div", _hoisted_31, [
                  createBaseVNode("div", _hoisted_32, [
                    createBaseVNode("div", _hoisted_33, [
                      _cache[20] || (_cache[20] = createBaseVNode("span", { class: "text-sm font-medium text-gray-700" }, "Total Processed:", -1)),
                      createBaseVNode("span", _hoisted_34, toDisplayString(processingResults.value.count), 1)
                    ])
                  ]),
                  createBaseVNode("div", _hoisted_35, [
                    (openBlock(true), createElementBlock(Fragment, null, renderList(processingResults.value.results, (result) => {
                      return openBlock(), createElementBlock("div", {
                        key: result.tx,
                        class: normalizeClass(["flex items-center justify-between p-2 rounded", getResultClass(result.status)])
                      }, [
                        createBaseVNode("span", _hoisted_36, toDisplayString(result.tx), 1),
                        createBaseVNode("span", _hoisted_37, toDisplayString(result.status), 1)
                      ], 2);
                    }), 128))
                  ])
                ]),
                createBaseVNode("div", _hoisted_38, [
                  createVNode(_component_Button, {
                    onClick: _cache[2] || (_cache[2] = ($event) => showResults.value = false),
                    theme: "gray",
                    variant: "outline"
                  }, {
                    default: withCtx(() => _cache[21] || (_cache[21] = [
                      createTextVNode(" Close ")
                    ])),
                    _: 1,
                    __: [21]
                  })
                ])
              ])
            ])) : createCommentVNode("", true)
          ])
        ]),
        showOfflineDialog.value ? (openBlock(), createElementBlock("div", _hoisted_39, [
          createBaseVNode("div", _hoisted_40, [
            createBaseVNode("div", {
              class: "fixed inset-0 bg-gray-900 bg-opacity-75",
              "aria-hidden": "true",
              onClick: _cache[3] || (_cache[3] = ($event) => showOfflineDialog.value = false)
            }),
            _cache[24] || (_cache[24] = createBaseVNode("span", {
              class: "hidden sm:inline-block sm:align-middle sm:h-screen",
              "aria-hidden": "true"
            }, "​", -1)),
            createBaseVNode("div", _hoisted_41, [
              _cache[23] || (_cache[23] = createStaticVNode('<div class="px-6 pt-6 pb-4" data-v-7b2d2de3><div class="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-red-100 mb-4" data-v-7b2d2de3><svg class="h-8 w-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" data-v-7b2d2de3><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M4.93 4.93l14.14 14.14M12 19c-3.866 0-7-3.134-7-7 0-1.657.57-3.178 1.52-4.382m1.53-1.53A6.978 6.978 0 0112 5c3.866 0 7 3.134 7 7 0 1.657-.57 3.178-1.52 4.382" data-v-7b2d2de3></path></svg></div><h3 class="text-xl font-bold text-gray-900 mb-2" data-v-7b2d2de3>No Internet Connection</h3><p class="text-sm text-gray-600" data-v-7b2d2de3>Please check/connect to the internet first and try again.</p></div>', 1)),
              createBaseVNode("div", _hoisted_42, [
                createBaseVNode("button", {
                  type: "button",
                  onClick: _cache[4] || (_cache[4] = ($event) => showOfflineDialog.value = false),
                  class: "w-full inline-flex justify-center rounded-lg border border-transparent shadow-sm px-6 py-3 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:w-auto"
                }, "OK")
              ])
            ])
          ])
        ])) : createCommentVNode("", true)
      ], 64);
    };
  }
};
const QRPayAdmin = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-7b2d2de3"]]);
export {
  QRPayAdmin as default
};
//# sourceMappingURL=QRPayAdmin-CMQYri2b.js.map
