var __defProp = Object.defineProperty;
var __getOwnPropSymbols = Object.getOwnPropertySymbols;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __propIsEnum = Object.prototype.propertyIsEnumerable;
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __spreadValues = (a, b) => {
  for (var prop in b || (b = {}))
    if (__hasOwnProp.call(b, prop))
      __defNormalProp(a, prop, b[prop]);
  if (__getOwnPropSymbols)
    for (var prop of __getOwnPropSymbols(b)) {
      if (__propIsEnum.call(b, prop))
        __defNormalProp(a, prop, b[prop]);
    }
  return a;
};
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
import { o as openBlock, a as createElementBlock, b as createBaseVNode, g as ref, c as computed, l as watch, k as onMounted, m as onUnmounted, t as toDisplayString, L as unref, I as createTextVNode, ad as createStaticVNode, z as createVNode, e as createCommentVNode, B as withDirectives, ac as vModelText, n as normalizeClass, F as Fragment, M as renderList, y as createBlock, q as nextTick } from "./vendor-DNPaXrxF.js";
import { j as _export_sfc, c as createResource, l as call, k as _sfc_main$2 } from "./ui-C-4uyU25.js";
import { s as session } from "./index-GzXbegLD.js";
const _hoisted_1$1 = { class: "fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50" };
const _sfc_main$1 = {
  __name: "LoadingOverlay",
  setup(__props) {
    return (_ctx, _cache) => {
      return openBlock(), createElementBlock("div", _hoisted_1$1, _cache[0] || (_cache[0] = [
        createBaseVNode("div", { class: "bg-white rounded-xl p-6 shadow-lg flex flex-col items-center space-y-2" }, [
          createBaseVNode("div", { class: "animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600" }),
          createBaseVNode("p", { class: "text-gray-700 font-medium" }, "Verifying Payment...")
        ], -1)
      ]));
    };
  }
};
const LoadingOverlay = /* @__PURE__ */ _export_sfc(_sfc_main$1, [["__scopeId", "data-v-d9fdddbf"]]);
const _hoisted_1 = { class: "min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50" };
const _hoisted_2 = { class: "bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20" };
const _hoisted_3 = { class: "max-w-5xl mx-auto px-4 sm:px-6 lg:px-8" };
const _hoisted_4 = { class: "flex justify-between items-center py-6" };
const _hoisted_5 = { class: "flex items-center space-x-4" };
const _hoisted_6 = { class: "text-sm text-gray-600" };
const _hoisted_7 = { class: "max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8" };
const _hoisted_8 = { class: "bg-white rounded-xl shadow-lg border border-gray-200 p-8" };
const _hoisted_9 = { class: "grid grid-cols-1 lg:grid-cols-2 gap-8" };
const _hoisted_10 = {
  key: 0,
  class: "mt-2 text-sm text-gray-500"
};
const _hoisted_11 = {
  key: 0,
  class: "space-y-3"
};
const _hoisted_12 = { class: "p-5 bg-gradient-to-r from-green-50 to-blue-50 border border-green-200 rounded-lg space-y-2" };
const _hoisted_13 = { class: "text-lg font-semibold text-gray-900" };
const _hoisted_14 = { class: "text-sm text-gray-600" };
const _hoisted_15 = {
  key: 0,
  class: "text-sm text-gray-600"
};
const _hoisted_16 = {
  key: 1,
  class: "text-sm text-gray-600"
};
const _hoisted_17 = {
  key: 2,
  class: "text-sm text-gray-600 whitespace-pre-line"
};
const _hoisted_18 = {
  key: 3,
  class: "text-sm text-gray-600"
};
const _hoisted_19 = {
  key: 4,
  class: "text-sm text-gray-600"
};
const _hoisted_20 = {
  key: 5,
  class: "text-sm text-gray-600"
};
const _hoisted_21 = { class: "bg-white rounded-xl shadow-lg border border-gray-200 p-8" };
const _hoisted_22 = { class: "grid grid-cols-1 md:grid-cols-2 gap-6" };
const _hoisted_23 = { class: "bg-white rounded-xl shadow-lg border border-gray-200 p-8 text-center" };
const _hoisted_24 = ["disabled"];
const _hoisted_25 = {
  key: 0,
  class: "animate-spin -ml-1 mr-3 h-5 w-5 text-white",
  xmlns: "http://www.w3.org/2000/svg",
  fill: "none",
  viewBox: "0 0 24 24"
};
const _hoisted_26 = {
  key: 1,
  class: "w-5 h-5 mr-3",
  fill: "none",
  stroke: "currentColor",
  viewBox: "0 0 24 24"
};
const _hoisted_27 = {
  key: 0,
  class: "bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl shadow-lg border-2 border-green-300 p-8 animate-pulse-slow"
};
const _hoisted_28 = { class: "text-center space-y-4" };
const _hoisted_29 = { class: "bg-white rounded-lg p-4 shadow-inner" };
const _hoisted_30 = { class: "text-4xl font-bold text-green-600" };
const _hoisted_31 = { class: "text-gray-700" };
const _hoisted_32 = { class: "font-semibold" };
const _hoisted_33 = {
  key: 0,
  class: "text-sm text-gray-600"
};
const _hoisted_34 = ["href"];
const _hoisted_35 = {
  key: 1,
  class: "bg-white rounded-xl shadow-lg border border-gray-200 p-8 space-y-6"
};
const _hoisted_36 = { class: "flex flex-col lg:flex-row lg:items-start lg:justify-between gap-6" };
const _hoisted_37 = { class: "flex-1 space-y-4" };
const _hoisted_38 = { class: "bg-gray-50 rounded-lg p-6 space-y-3" };
const _hoisted_39 = { class: "text-center" };
const _hoisted_40 = { class: "border-t border-gray-200 pt-3 space-y-2" };
const _hoisted_41 = { class: "flex justify-between text-sm" };
const _hoisted_42 = { class: "font-semibold" };
const _hoisted_43 = { class: "flex justify-between text-sm" };
const _hoisted_44 = { class: "font-semibold truncate ml-2" };
const _hoisted_45 = {
  key: 0,
  class: "flex justify-between text-sm"
};
const _hoisted_46 = ["href"];
const _hoisted_47 = { class: "flex items-start" };
const _hoisted_48 = {
  key: 0,
  class: "w-5 h-5 text-orange-600 mr-2 mt-0.5",
  fill: "none",
  stroke: "currentColor",
  viewBox: "0 0 24 24"
};
const _hoisted_49 = {
  key: 1,
  class: "w-5 h-5 text-yellow-600 mr-2 mt-0.5",
  fill: "none",
  stroke: "currentColor",
  viewBox: "0 0 24 24"
};
const _hoisted_50 = {
  key: 2,
  class: "w-5 h-5 text-red-600 mr-2 mt-0.5",
  fill: "none",
  stroke: "currentColor",
  viewBox: "0 0 24 24"
};
const _hoisted_51 = { class: "flex-1" };
const _hoisted_52 = { class: "flex gap-3" };
const _hoisted_53 = ["disabled"];
const _hoisted_54 = {
  key: 2,
  class: "bg-white rounded-xl shadow-lg border border-gray-200 p-8"
};
const _hoisted_55 = { class: "space-y-3 max-h-72 overflow-y-auto pr-1" };
const _hoisted_56 = { class: "flex justify-between items-center mb-1" };
const _hoisted_57 = { class: "text-xs text-gray-500" };
const _hoisted_58 = { class: "text-sm text-gray-700 whitespace-pre-line break-words" };
const _hoisted_59 = {
  key: 3,
  class: "fixed inset-0 z-50 overflow-y-auto",
  "aria-labelledby": "modal-title",
  role: "dialog",
  "aria-modal": "true"
};
const _hoisted_60 = { class: "flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0" };
const _hoisted_61 = { class: "inline-block align-bottom bg-white rounded-2xl text-left overflow-hidden shadow-2xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full" };
const _hoisted_62 = { class: "bg-white px-6 pt-6 pb-4" };
const _hoisted_63 = { class: "text-center" };
const _hoisted_64 = { class: "mt-4 mb-6" };
const _hoisted_65 = { class: "bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-6 border-2 border-green-200" };
const _hoisted_66 = { class: "text-5xl font-bold text-green-600" };
const _hoisted_67 = { class: "mt-4 space-y-2" };
const _hoisted_68 = { class: "text-sm text-gray-600" };
const _hoisted_69 = {
  key: 0,
  class: "text-sm text-gray-600"
};
const _hoisted_70 = ["href"];
const _hoisted_71 = { class: "text-xs text-gray-500 mt-2" };
const _hoisted_72 = { class: "bg-gray-50 px-6 py-4 sm:flex sm:flex-row-reverse gap-3" };
const _hoisted_73 = {
  key: 4,
  class: "bg-white rounded-xl shadow-lg border border-red-200 p-8"
};
const _hoisted_74 = { class: "text-center space-y-4" };
const _hoisted_75 = { class: "text-gray-600" };
const _sfc_main = {
  __name: "QRPay",
  setup(__props) {
    const selectedCustomer = ref(null);
    const selectedCustomerValue = ref(null);
    const customerOptions = ref([]);
    const loadingCustomers = ref(false);
    const paymentAmount = ref("");
    const remarks = ref("");
    const generating = ref(false);
    const qrData = ref(null);
    const qrStatus = ref(null);
    const paymentEntry = ref(null);
    const websocketUrl = ref("");
    const merchantWebsocketUrl = ref("");
    const statusLogs = ref([]);
    const showLoadingOverlay = ref(false);
    const showSuccessDialog = ref(false);
    const showErrorDialog = ref(false);
    const paymentMessage = ref("");
    const customerSearchResource = createResource({
      url: "custom_erp.custom_erp.api.fonepay.search_customers",
      auto: false
    });
    const qrCreateResource = createResource({ url: "custom_erp.custom_erp.api.fonepay.create_dynamic_qr", auto: false });
    let realtimeHandler = null;
    const merchantSocket = ref(null);
    const currentTxName = ref(null);
    const canGenerate = computed(() => {
      var _a;
      const amount = Number(paymentAmount.value);
      const result = Boolean(selectedCustomer.value && amount > 0);
      console.log("canGenerate check:", {
        hasCustomer: !!selectedCustomer.value,
        customerName: (_a = selectedCustomer.value) == null ? void 0 : _a.name,
        amount,
        result
      });
      return result;
    });
    const statusColorClass = computed(() => getStatusColor(qrStatus.value));
    watch(selectedCustomerValue, (newValue) => {
      console.log("selectedCustomerValue changed:", newValue);
      if (!newValue) {
        selectedCustomer.value = null;
        return;
      }
      let option = null;
      if (typeof newValue === "object" && newValue !== null) {
        option = newValue;
      } else {
        option = customerOptions.value.find((opt) => opt.value === newValue);
      }
      console.log("Found option:", option);
      if (option) {
        selectedCustomer.value = {
          name: option.value || option.name,
          customer_name: option.customer_name,
          customer_group: option.customer_group,
          territory: option.territory,
          customer_primary_address: option.customer_primary_address,
          address_display: option.address_display,
          mobile_no: option.mobile_no,
          email_id: option.email_id
        };
        console.log("Set selectedCustomer:", selectedCustomer.value);
        pushStatusLog("info", `Selected customer ${selectedCustomer.value.customer_name} (${selectedCustomer.value.name})`);
      }
    });
    const loadCustomers = (query = "") => __async(this, null, function* () {
      var _a;
      loadingCustomers.value = true;
      try {
        const response = yield customerSearchResource.fetch({ query, limit: 1e4 });
        const payload = (response == null ? void 0 : response.customers) || ((_a = response == null ? void 0 : response.message) == null ? void 0 : _a.customers) || [];
        customerOptions.value = payload.map((customer) => __spreadValues({
          label: `${customer.customer_name} (${customer.name})`,
          value: customer.name
        }, customer));
      } catch (error) {
        console.error("Error loading customers", error);
      } finally {
        loadingCustomers.value = false;
      }
    });
    const generateQR = () => __async(this, null, function* () {
      var _a;
      if (!canGenerate.value || generating.value) {
        return;
      }
      generating.value = true;
      qrData.value = null;
      qrStatus.value = null;
      paymentEntry.value = null;
      websocketUrl.value = "";
      merchantWebsocketUrl.value = "";
      currentTxName.value = null;
      clearRealtime();
      closeMerchantSocket();
      pushStatusLog("info", "Submitting request to generate QR code...");
      try {
        const amount = Number(paymentAmount.value) || 0;
        const remarksValue = ((_a = remarks.value) == null ? void 0 : _a.trim()) || "";
        const response = yield qrCreateResource.fetch({
          amount,
          customer: selectedCustomer.value.name,
          remarks1: remarksValue,
          remarks2: ""
        });
        if (!(response == null ? void 0 : response.qr_message)) {
          throw new Error("No QR message returned by Fonepay");
        }
        qrData.value = response;
        qrStatus.value = response.status || "CREATED";
        websocketUrl.value = response.websocket_url || "";
        merchantWebsocketUrl.value = response.merchant_websocket_url || "";
        currentTxName.value = response.tx_name;
        pushStatusLog("success", "QR code created successfully. Awaiting payment events...");
        yield renderQRCode(response.qr_message);
        yield nextTick();
        yield nextTick();
        yield new Promise((resolve) => setTimeout(resolve, 300));
        subscribeToUpdates(response.tx_name);
        yield connectMerchantSocketRobust(response.merchant_websocket_url || response.websocket_url);
      } catch (error) {
        console.error("Error generating QR", error);
        pushStatusLog("error", `Failed to generate QR code: ${error.message || error}`);
        alert(`Failed to generate QR code: ${error.message || error}`);
      } finally {
        generating.value = false;
      }
    });
    const renderQRCode = (qrMessage) => __async(this, null, function* () {
      if (!qrMessage) return;
      if (!window.QRCode) {
        const script = document.createElement("script");
        script.src = "https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js";
        document.head.appendChild(script);
        yield new Promise((resolve) => {
          script.onload = resolve;
          script.onerror = resolve;
        });
      }
      yield new Promise((resolve) => setTimeout(resolve, 100));
      const qrContainer = document.getElementById("qr-code");
      if (qrContainer) {
        qrContainer.innerHTML = "";
        void qrContainer.offsetHeight;
        try {
          new window.QRCode(qrContainer, {
            text: qrMessage,
            width: 256,
            height: 256,
            correctLevel: window.QRCode.CorrectLevel.M
          });
          console.log("✅ QR code rendered successfully");
          pushStatusLog("success", "QR code displayed.");
        } catch (error) {
          console.error("Unable to render QR code", error);
          pushStatusLog("error", "Unable to render QR code in the browser.");
        }
      } else {
        console.warn("⚠️ QR container element not found");
        pushStatusLog("warning", "QR container not ready, retrying...");
        yield new Promise((resolve) => setTimeout(resolve, 300));
        const retryContainer = document.getElementById("qr-code");
        if (retryContainer) {
          retryContainer.innerHTML = "";
          try {
            new window.QRCode(retryContainer, {
              text: qrMessage,
              width: 256,
              height: 256,
              correctLevel: window.QRCode.CorrectLevel.M
            });
            console.log("✅ QR code rendered on retry");
          } catch (error) {
            console.error("Unable to render QR code on retry", error);
          }
        }
      }
    });
    const connectMerchantSocketRobust = (url) => __async(this, null, function* () {
      console.log("🚀 [WEBSOCKET-ROBUST] ================================================");
      console.log("🚀 [WEBSOCKET-ROBUST] Starting BULLETPROOF connection sequence");
      console.log("🚀 [WEBSOCKET-ROBUST] URL:", url);
      console.log("🚀 [WEBSOCKET-ROBUST] Time:", (/* @__PURE__ */ new Date()).toISOString());
      console.log("🚀 [WEBSOCKET-ROBUST] ================================================");
      if (!url || typeof WebSocket === "undefined") {
        console.error("❌ [WEBSOCKET-ROBUST] Invalid parameters - cannot connect");
        pushStatusLog("error", "WebSocket unavailable or URL missing");
        return Promise.reject(new Error("WebSocket unavailable"));
      }
      closeMerchantSocket();
      pushStatusLog("info", "🔌 Initializing merchant websocket connection...");
      return new Promise((resolve, reject) => {
        try {
          const ws = new WebSocket(url);
          merchantSocket.value = ws;
          console.log("✓ [WEBSOCKET-ROBUST] Socket instance created and stored");
          console.log("✓ [WEBSOCKET-ROBUST] Initial readyState:", ws.readyState, "(0=CONNECTING)");
          const connectionTimeout = setTimeout(() => {
            if (ws.readyState !== WebSocket.OPEN) {
              console.error("⏱️ [WEBSOCKET-ROBUST] Connection timeout!");
              ws.close();
              merchantSocket.value = null;
              reject(new Error("WebSocket connection timeout"));
            }
          }, 3e4);
          ws.onopen = () => {
            clearTimeout(connectionTimeout);
            console.log("✅ [WEBSOCKET-ROBUST] ====== CONNECTION ESTABLISHED ======");
            console.log("✅ [WEBSOCKET-ROBUST] ReadyState:", ws.readyState, "(1=OPEN)");
            console.log("✅ [WEBSOCKET-ROBUST] Socket stored:", !!merchantSocket.value);
            console.log("✅ [WEBSOCKET-ROBUST] Ready to receive messages!");
            console.log("✅ [WEBSOCKET-ROBUST] ====================================");
            pushStatusLog("success", "✅ Merchant websocket CONNECTED and READY!");
            resolve(ws);
          };
          ws.onerror = (event) => {
            clearTimeout(connectionTimeout);
            console.error("❌ [WEBSOCKET-ROBUST] Error event:", event);
            console.error("❌ [WEBSOCKET-ROBUST] ReadyState:", ws.readyState);
            pushStatusLog("error", "❌ WebSocket connection error");
          };
          ws.onclose = (event) => {
            clearTimeout(connectionTimeout);
            console.log("🔌 [WEBSOCKET-ROBUST] Connection closed");
            console.log("🔌 [WEBSOCKET-ROBUST] Code:", event.code);
            console.log("🔌 [WEBSOCKET-ROBUST] Reason:", event.reason);
            console.log("🔌 [WEBSOCKET-ROBUST] Clean:", event.wasClean);
            merchantSocket.value = null;
            pushStatusLog("warning", `WebSocket disconnected (${event.code})`);
            if (ws.readyState !== WebSocket.OPEN) {
              reject(new Error(`WebSocket closed before opening (code: ${event.code})`));
            }
          };
          ws.onmessage = (event) => __async(this, null, function* () {
            console.log("🎉 [WEBSOCKET-ROBUST] ================================================");
            console.log("🎉 [WEBSOCKET-ROBUST] ⚡ MESSAGE RECEIVED ⚡");
            console.log("🎉 [WEBSOCKET-ROBUST] Time:", (/* @__PURE__ */ new Date()).toISOString());
            console.log("🎉 [WEBSOCKET-ROBUST] Socket state:", ws.readyState);
            console.log("🎉 [WEBSOCKET-ROBUST] Stored ref valid:", !!merchantSocket.value);
            console.log("🎉 [WEBSOCKET-ROBUST] Raw data:", event.data);
            console.log("🎉 [WEBSOCKET-ROBUST] ================================================");
            pushStatusLog("ws", `📨 WS Message: ${event.data}`);
            let data = null;
            try {
              data = JSON.parse(event.data || "{}");
              console.log("📦 [WEBSOCKET-ROBUST] Parsed data:", JSON.stringify(data, null, 2));
            } catch (error) {
              console.warn("⚠️ [WEBSOCKET-ROBUST] Non-JSON message, ignoring");
              return;
            }
            if (data && typeof data === "object") {
              console.log("🔍 [WEBSOCKET-ROBUST] Processing payment data...");
              console.log("🔍 [WEBSOCKET-ROBUST] Fields:", Object.keys(data));
              console.log("🔍 [WEBSOCKET-ROBUST] transactionStatus:", data.transactionStatus);
              console.log("🔍 [WEBSOCKET-ROBUST] productNumber:", data.productNumber);
              yield handleWebSocketPaymentUpdate(data);
            }
          });
          console.log("✓ [WEBSOCKET-ROBUST] All handlers attached successfully");
          console.log("✓ [WEBSOCKET-ROBUST] Waiting for connection to open...");
        } catch (error) {
          console.error("❌ [WEBSOCKET-ROBUST] Exception during setup:", error);
          merchantSocket.value = null;
          pushStatusLog("error", `WebSocket setup failed: ${error.message}`);
          reject(error);
        }
      });
    });
    const handleWebSocketPaymentUpdate = (data) => __async(this, null, function* () {
      try {
        console.log("💳 [PAYMENT-UPDATE] ========== PROCESSING PAYMENT UPDATE ==========");
        console.log("💳 [PAYMENT-UPDATE] Raw data:", JSON.stringify(data, null, 2));
        let isSuccess = false;
        let isFailed = false;
        let isScanned = false;
        let parsedStatus = null;
        if (data.transactionStatus && typeof data.transactionStatus === "string") {
          try {
            parsedStatus = JSON.parse(data.transactionStatus);
            console.log("💳 [PAYMENT-UPDATE] Parsed transactionStatus:", parsedStatus);
            if (parsedStatus.qrVerified === true && parsedStatus.paymentSuccess !== true) {
              isScanned = true;
              console.log("💳 [PAYMENT-UPDATE] ✅ QR VERIFIED (scanned but not paid)");
            } else if (parsedStatus.paymentSuccess === true || parsedStatus.success === true) {
              isSuccess = true;
              console.log("💳 [PAYMENT-UPDATE] ✅ PAYMENT SUCCESS!");
            } else if (parsedStatus.paymentSuccess === false || parsedStatus.success === false) {
              isFailed = true;
              console.log("💳 [PAYMENT-UPDATE] ❌ PAYMENT FAILED");
            }
          } catch (e) {
            console.warn("💳 [PAYMENT-UPDATE] Could not parse transactionStatus as JSON:", e);
          }
        }
        if (!isSuccess && !isFailed && data.transactionStatus && typeof data.transactionStatus === "object") {
          const status = String(data.transactionStatus).toUpperCase();
          console.log("💳 [PAYMENT-UPDATE] Object status:", status);
          isSuccess = status === "SUCCESS" || status === "COMPLETED";
          isFailed = status === "FAILED";
          isScanned = status === "INITIATED" || status === "VERIFIED";
        }
        if (!isSuccess && !isFailed) {
          isSuccess = data.paymentSuccess === true || data.success === true;
          isFailed = data.paymentSuccess === false || data.success === false;
        }
        console.log("💳 [PAYMENT-UPDATE] Status flags:", { isSuccess, isFailed, isScanned });
        if (isSuccess) {
          console.log("🎉 [PAYMENT-UPDATE] ========== PAYMENT SUCCESS DETECTED! ==========");
          showLoadingOverlay.value = true;
          pushStatusLog("success", "🎉 Payment success detected! Verifying with backend...");
          try {
            const prnRef = parsedStatus ? String(parsedStatus.productNumber || parsedStatus.prn || "") : "";
            console.log("💳 [PAYMENT-UPDATE] PRN for verification:", prnRef);
            console.log("💳 [PAYMENT-UPDATE] Calling check_status API...");
            const verify = yield call("custom_erp.custom_erp.api.fonepay.check_status", {
              txn_ref_id: prnRef || currentTxName.value
            });
            console.log("💳 [PAYMENT-UPDATE] Backend verification response:", verify);
            if (verify && verify.status === "SUCCESS") {
              console.log("✅ [PAYMENT-UPDATE] Backend confirmed SUCCESS!");
              qrStatus.value = "SUCCESS";
              paymentEntry.value = verify.payment_entry || paymentEntry.value;
              paymentMessage.value = "Payment confirmed successfully! Amount: NPR " + formatAmount(paymentAmount.value);
              pushStatusLog("success", "✅ Backend verification complete. Payment Entry: " + paymentEntry.value);
              removeQrAndShowSuccess();
            } else {
              console.error("❌ [PAYMENT-UPDATE] Backend verification failed!");
              qrStatus.value = "FAILED";
              paymentMessage.value = "Verification failed: " + ((verify == null ? void 0 : verify.message) || "Unknown error");
              pushStatusLog("error", "❌ Backend verification failed: " + paymentMessage.value);
              showFailedDialog();
            }
          } catch (error) {
            console.error("❌ [PAYMENT-UPDATE] Verification error:", error);
            qrStatus.value = "FAILED";
            paymentMessage.value = "Verification error: " + (error.message || error);
            pushStatusLog("error", "❌ Verification API error: " + paymentMessage.value);
            showFailedDialog();
          } finally {
            showLoadingOverlay.value = false;
          }
        } else if (isFailed) {
          console.log("❌ [PAYMENT-UPDATE] ========== PAYMENT FAILED ==========");
          showLoadingOverlay.value = false;
          qrStatus.value = "FAILED";
          paymentMessage.value = data.responseMessage || data.message || "Payment failed.";
          pushStatusLog("error", "❌ Payment failed: " + paymentMessage.value);
          showFailedDialog();
        } else if (isScanned) {
          console.log("👀 [PAYMENT-UPDATE] ========== QR SCANNED ==========");
          qrStatus.value = "SCANNED";
          pushStatusLog("info", "👀 QR code scanned by customer. Waiting for payment confirmation...");
        } else {
          console.log("ℹ️ [PAYMENT-UPDATE] Other status update");
          pushStatusLog("info", "Payment status update: " + JSON.stringify(data.transactionStatus));
        }
        console.log("💳 [PAYMENT-UPDATE] ========== UPDATE PROCESSING COMPLETE ==========");
      } catch (error) {
        console.error("❌ [PAYMENT-UPDATE] Error processing update:", error);
        pushStatusLog("error", `Error processing payment update: ${error.message}`);
        showLoadingOverlay.value = false;
      }
    });
    const subscribeToUpdates = (txName) => {
      if (!(window.frappe && frappe.realtime)) {
        pushStatusLog("warning", "Realtime channel is unavailable in this session.");
        return;
      }
      clearRealtime();
      realtimeHandler = (data) => {
        if (!data || data.tx !== txName) {
          return;
        }
        processRealtimeUpdate(data);
      };
      frappe.realtime.on("fonepay_update", realtimeHandler);
    };
    const processRealtimeUpdate = (data) => {
      if (!data) return;
      if (data.transactionStatus) {
        const ts = String(data.transactionStatus).toUpperCase();
        if (ts === "SUCCESS" || ts === "COMPLETED") {
          qrStatus.value = "SUCCESS";
        } else if (ts === "FAILED") {
          qrStatus.value = "FAILED";
        } else if (ts === "INITIATED") {
          qrStatus.value = "SCANNED";
        } else {
          qrStatus.value = ts;
        }
      } else if (data.status) {
        qrStatus.value = data.status;
      }
      if (data.payment_entry) {
        paymentEntry.value = data.payment_entry;
      }
      const statusMsg = data.status || data.transactionStatus || "Unknown";
      pushStatusLog("event", data.message || `Status updated: ${statusMsg}`, JSON.stringify(data, null, 2));
      if (data.status === "SUCCESS" || data.transactionStatus && String(data.transactionStatus).toUpperCase() === "SUCCESS") {
        pushStatusLog("success", "Payment successful! Payment Entry has been created and submitted.");
      }
    };
    const clearRealtime = () => {
      if (window.frappe && frappe.realtime && realtimeHandler) {
        frappe.realtime.off("fonepay_update", realtimeHandler);
      }
      realtimeHandler = null;
    };
    const closeMerchantSocket = () => {
      if (merchantSocket.value) {
        try {
          merchantSocket.value.close();
        } catch (error) {
          console.warn("Error closing websocket", error);
        }
      }
      merchantSocket.value = null;
    };
    const regenerateQR = () => {
      qrData.value = null;
      qrStatus.value = null;
      paymentEntry.value = null;
      websocketUrl.value = "";
      merchantWebsocketUrl.value = "";
      currentTxName.value = null;
      clearRealtime();
      closeMerchantSocket();
      pushStatusLog("info", "State reset. Ready to generate a new QR code.");
    };
    const manuallyProcessPayment = () => __async(this, null, function* () {
      if (!currentTxName.value) {
        alert("No transaction to process");
        return;
      }
      pushStatusLog("info", "Manually triggering payment processing...");
      showLoadingOverlay.value = true;
      try {
        console.log("🔍 Calling check_status API with txn_ref_id:", currentTxName.value);
        const verify = yield call("custom_erp.custom_erp.api.fonepay.check_status", {
          txn_ref_id: currentTxName.value
        });
        console.log("✅ Manual verification response:", verify);
        console.log("Response type:", typeof verify, "Keys:", Object.keys(verify || {}));
        pushStatusLog("info", "Backend verification response: " + JSON.stringify(verify, null, 2));
        if (verify && verify.status === "SUCCESS") {
          qrStatus.value = "SUCCESS";
          paymentEntry.value = verify.payment_entry;
          paymentMessage.value = "Payment processed successfully.";
          pushStatusLog("success", "Payment Entry created: " + paymentEntry.value);
          removeQrAndShowSuccess();
        } else if (verify && verify.status === "VERIFIED_NOT_PAID") {
          qrStatus.value = "SCANNED";
          pushStatusLog("info", "QR code has been scanned/verified but payment not yet completed.");
          paymentMessage.value = verify.message || "✅ QR Code Scanned! Customer has opened their payment app but has not completed the payment yet. Please wait for them to confirm and complete the payment. Keep this QR visible.";
        } else if (verify && verify.status === "PENDING") {
          qrStatus.value = "PENDING";
          pushStatusLog("warning", "Payment is still pending. Customer may not have scanned QR yet.");
          paymentMessage.value = verify.message || "⏳ Payment Pending. Customer has not yet scanned the QR code. Please ask the customer to scan and pay. Keep this QR visible.";
        } else if (verify && verify.status === "FAILED") {
          qrStatus.value = "FAILED";
          pushStatusLog("error", "Payment failed: " + (verify.message || "Payment was declined or cancelled"));
          paymentMessage.value = verify.message || "❌ Payment Failed. The payment was declined or cancelled by the customer. You may need to generate a new QR code.";
          showFailedDialog();
        } else if (verify && verify.status === "ERROR") {
          qrStatus.value = "ERROR";
          pushStatusLog("error", "Payment verification error: " + (verify.message || "Unknown error"));
          paymentMessage.value = verify.message || "⚠️ Verification Error. Unable to verify payment status with Fonepay. Please check the transaction manually or try again.";
        } else {
          qrStatus.value = "UNKNOWN";
          pushStatusLog("error", "Unexpected response: " + JSON.stringify(verify));
          paymentMessage.value = "❓ Unknown Status. Received unexpected response from server. Please check status logs or contact support.";
        }
      } catch (error) {
        console.error("❌ Manual processing error:", error);
        pushStatusLog("error", "Error processing payment: " + (error.message || JSON.stringify(error)));
        alert("Error processing payment: " + (error.message || JSON.stringify(error)));
      } finally {
        showLoadingOverlay.value = false;
      }
    });
    const removeQrAndShowSuccess = () => {
      qrData.value = null;
      showSuccessDialog.value = true;
      closeMerchantSocket();
      clearRealtime();
      pushStatusLog("success", "Payment successfully verified and processed!");
    };
    const showFailedDialog = () => {
      qrData.value = null;
      showErrorDialog.value = true;
    };
    const resetForNextPayment = () => {
      showSuccessDialog.value = false;
      paymentAmount.value = "";
      remarks.value = "";
      qrStatus.value = null;
      paymentEntry.value = null;
      statusLogs.value = [];
      pushStatusLog("info", "Ready for next payment.");
    };
    const regenerateQRFromDialog = () => {
      showErrorDialog.value = false;
      qrData.value = null;
      qrStatus.value = null;
      paymentEntry.value = null;
      websocketUrl.value = "";
      merchantWebsocketUrl.value = "";
      currentTxName.value = null;
      clearRealtime();
      closeMerchantSocket();
      pushStatusLog("info", "Ready to regenerate QR code.");
    };
    const resetAll = () => {
      showErrorDialog.value = false;
      showSuccessDialog.value = false;
      selectedCustomer.value = null;
      selectedCustomerValue.value = null;
      paymentAmount.value = "";
      remarks.value = "";
      qrData.value = null;
      qrStatus.value = null;
      paymentEntry.value = null;
      websocketUrl.value = "";
      merchantWebsocketUrl.value = "";
      currentTxName.value = null;
      statusLogs.value = [];
      clearRealtime();
      closeMerchantSocket();
      pushStatusLog("info", "Reset complete. Ready for new transaction.");
    };
    const pushStatusLog = (level, message, payload = null) => {
      const entry = {
        id: `${Date.now()}-${Math.random()}`,
        ts: /* @__PURE__ */ new Date(),
        level,
        message,
        payload,
        levelLabel: levelLabel(level),
        levelClass: levelClass(level)
      };
      statusLogs.value.unshift(entry);
      if (statusLogs.value.length > 30) {
        statusLogs.value.pop();
      }
    };
    const levelLabel = (level) => {
      switch (level) {
        case "error":
          return "Error";
        case "warning":
          return "Warning";
        case "success":
          return "Success";
        case "event":
          return "Realtime Event";
        case "ws":
          return "Websocket";
        default:
          return "Info";
      }
    };
    const levelClass = (level) => {
      switch (level) {
        case "error":
          return "text-red-600";
        case "warning":
          return "text-yellow-600";
        case "success":
          return "text-green-600";
        case "event":
          return "text-blue-600";
        case "ws":
          return "text-purple-600";
        default:
          return "text-gray-600";
      }
    };
    const getStatusColor = (status) => {
      switch ((status || "").toUpperCase()) {
        case "CREATED":
          return "text-blue-600";
        case "SCANNED":
          return "text-yellow-600";
        case "VERIFIED":
          return "text-indigo-600";
        case "PENDING":
          return "text-orange-600";
        case "SUCCESS":
          return "text-green-600";
        case "FAILED":
          return "text-red-600";
        case "ERROR":
          return "text-red-700";
        case "UNKNOWN":
          return "text-gray-500";
        default:
          return "text-gray-600";
      }
    };
    const formatAmount = (amount) => {
      const num = Number(amount) || 0;
      return num.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    };
    const formatLogTime = (ts) => {
      return new Date(ts).toLocaleString();
    };
    onMounted(() => __async(this, null, function* () {
      yield loadCustomers();
      pushStatusLog("info", "Ready to generate Fonepay QR codes for customers.");
    }));
    onUnmounted(() => {
      clearRealtime();
      closeMerchantSocket();
    });
    return (_ctx, _cache) => {
      var _a, _b, _c;
      return openBlock(), createElementBlock("div", _hoisted_1, [
        createBaseVNode("header", _hoisted_2, [
          createBaseVNode("div", _hoisted_3, [
            createBaseVNode("div", _hoisted_4, [
              createBaseVNode("div", _hoisted_5, [
                _cache[7] || (_cache[7] = createBaseVNode("div", { class: "flex items-center justify-center w-12 h-12 bg-blue-600 rounded-lg" }, [
                  createBaseVNode("svg", {
                    class: "w-6 h-6 text-white",
                    fill: "none",
                    stroke: "currentColor",
                    viewBox: "0 0 24 24"
                  }, [
                    createBaseVNode("path", {
                      "stroke-linecap": "round",
                      "stroke-linejoin": "round",
                      "stroke-width": "2",
                      d: "M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0a9 9 0 11-18 0 9 9 0 0118 0z"
                    })
                  ])
                ], -1)),
                createBaseVNode("div", null, [
                  _cache[6] || (_cache[6] = createBaseVNode("h1", { class: "text-2xl font-bold text-gray-900" }, "QRPay", -1)),
                  createBaseVNode("p", _hoisted_6, "Dynamic Fonepay QR Generator • " + toDisplayString(unref(session).user), 1)
                ])
              ]),
              createBaseVNode("button", {
                onClick: _cache[0] || (_cache[0] = ($event) => unref(session).logout.submit()),
                class: "inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              }, _cache[8] || (_cache[8] = [
                createBaseVNode("svg", {
                  class: "w-4 h-4 mr-2",
                  fill: "none",
                  stroke: "currentColor",
                  viewBox: "0 0 24 24"
                }, [
                  createBaseVNode("path", {
                    "stroke-linecap": "round",
                    "stroke-linejoin": "round",
                    "stroke-width": "2",
                    d: "M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                  })
                ], -1),
                createTextVNode(" Logout ")
              ]))
            ])
          ])
        ]),
        createBaseVNode("main", _hoisted_7, [
          createBaseVNode("section", _hoisted_8, [
            _cache[11] || (_cache[11] = createStaticVNode('<div class="flex items-center mb-6" data-v-1308ca85><div class="flex items-center justify-center w-10 h-10 bg-green-100 rounded-lg mr-3" data-v-1308ca85><svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" data-v-1308ca85><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" data-v-1308ca85></path></svg></div><h2 class="text-xl font-semibold text-gray-900" data-v-1308ca85>Customer</h2></div>', 1)),
            createBaseVNode("div", _hoisted_9, [
              createBaseVNode("div", null, [
                _cache[9] || (_cache[9] = createBaseVNode("label", { class: "block text-sm font-semibold text-gray-700 mb-3" }, "Select Customer", -1)),
                createVNode(unref(_sfc_main$2), {
                  modelValue: selectedCustomerValue.value,
                  "onUpdate:modelValue": _cache[1] || (_cache[1] = ($event) => selectedCustomerValue.value = $event),
                  options: customerOptions.value,
                  loading: loadingCustomers.value,
                  placeholder: "Search by customer name or code",
                  class: "w-full"
                }, null, 8, ["modelValue", "options", "loading"]),
                !selectedCustomer.value ? (openBlock(), createElementBlock("p", _hoisted_10, "Start typing to search every customer by name or code. All customers are available.")) : createCommentVNode("", true)
              ]),
              selectedCustomer.value ? (openBlock(), createElementBlock("div", _hoisted_11, [
                _cache[10] || (_cache[10] = createBaseVNode("label", { class: "block text-sm font-semibold text-gray-700" }, "Customer Details", -1)),
                createBaseVNode("div", _hoisted_12, [
                  createBaseVNode("div", _hoisted_13, toDisplayString(selectedCustomer.value.customer_name), 1),
                  createBaseVNode("div", _hoisted_14, "Customer Code: " + toDisplayString(selectedCustomer.value.name), 1),
                  selectedCustomer.value.customer_group ? (openBlock(), createElementBlock("div", _hoisted_15, "Group: " + toDisplayString(selectedCustomer.value.customer_group), 1)) : createCommentVNode("", true),
                  selectedCustomer.value.territory ? (openBlock(), createElementBlock("div", _hoisted_16, "Territory: " + toDisplayString(selectedCustomer.value.territory), 1)) : createCommentVNode("", true),
                  selectedCustomer.value.address_display ? (openBlock(), createElementBlock("div", _hoisted_17, toDisplayString(selectedCustomer.value.address_display), 1)) : selectedCustomer.value.customer_primary_address ? (openBlock(), createElementBlock("div", _hoisted_18, " Address: " + toDisplayString(selectedCustomer.value.customer_primary_address), 1)) : createCommentVNode("", true),
                  selectedCustomer.value.mobile_no ? (openBlock(), createElementBlock("div", _hoisted_19, "Phone: " + toDisplayString(selectedCustomer.value.mobile_no), 1)) : createCommentVNode("", true),
                  selectedCustomer.value.email_id ? (openBlock(), createElementBlock("div", _hoisted_20, "Email: " + toDisplayString(selectedCustomer.value.email_id), 1)) : createCommentVNode("", true)
                ])
              ])) : createCommentVNode("", true)
            ])
          ]),
          createBaseVNode("section", _hoisted_21, [
            _cache[14] || (_cache[14] = createStaticVNode('<div class="flex items-center mb-6" data-v-1308ca85><div class="flex items-center justify-center w-10 h-10 bg-orange-100 rounded-lg mr-3" data-v-1308ca85><svg class="w-5 h-5 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" data-v-1308ca85><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" data-v-1308ca85></path></svg></div><h2 class="text-xl font-semibold text-gray-900" data-v-1308ca85>Payment Details</h2></div>', 1)),
            createBaseVNode("div", _hoisted_22, [
              createBaseVNode("div", null, [
                _cache[12] || (_cache[12] = createBaseVNode("label", { class: "block text-sm font-semibold text-gray-700 mb-3" }, "Amount (NPR)", -1)),
                withDirectives(createBaseVNode("input", {
                  "onUpdate:modelValue": _cache[2] || (_cache[2] = ($event) => paymentAmount.value = $event),
                  type: "number",
                  step: "0.01",
                  min: "0",
                  placeholder: "Enter amount to collect",
                  class: "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                }, null, 512), [
                  [
                    vModelText,
                    paymentAmount.value,
                    void 0,
                    { number: true }
                  ]
                ])
              ]),
              createBaseVNode("div", null, [
                _cache[13] || (_cache[13] = createBaseVNode("label", { class: "block text-sm font-semibold text-gray-700 mb-3" }, "Remarks (optional)", -1)),
                withDirectives(createBaseVNode("input", {
                  "onUpdate:modelValue": _cache[3] || (_cache[3] = ($event) => remarks.value = $event),
                  type: "text",
                  placeholder: "Defaults to: Customer Name - NPR Amount (Date & Time)",
                  class: "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                }, null, 512), [
                  [vModelText, remarks.value]
                ])
              ])
            ])
          ]),
          createBaseVNode("section", _hoisted_23, [
            createBaseVNode("button", {
              onClick: generateQR,
              disabled: !canGenerate.value || generating.value,
              class: normalizeClass([
                "inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-lg shadow-sm text-white focus:outline-none focus:ring-2 focus:ring-offset-2 transition-all duration-200",
                canGenerate.value && !generating.value ? "bg-blue-600 hover:bg-blue-700 focus:ring-blue-500 shadow-lg hover:shadow-xl" : "bg-gray-400 cursor-not-allowed"
              ])
            }, [
              generating.value ? (openBlock(), createElementBlock("svg", _hoisted_25, _cache[15] || (_cache[15] = [
                createBaseVNode("circle", {
                  class: "opacity-25",
                  cx: "12",
                  cy: "12",
                  r: "10",
                  stroke: "currentColor",
                  "stroke-width": "4"
                }, null, -1),
                createBaseVNode("path", {
                  class: "opacity-75",
                  fill: "currentColor",
                  d: "M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                }, null, -1)
              ]))) : (openBlock(), createElementBlock("svg", _hoisted_26, _cache[16] || (_cache[16] = [
                createBaseVNode("path", {
                  "stroke-linecap": "round",
                  "stroke-linejoin": "round",
                  "stroke-width": "2",
                  d: "M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0a9 9 0 11-18 0 9 9 0 0118 0z"
                }, null, -1)
              ]))),
              createTextVNode(" " + toDisplayString(generating.value ? "Generating QR Code..." : "Generate Customer QR Code"), 1)
            ], 10, _hoisted_24)
          ]),
          qrStatus.value === "SUCCESS" && paymentEntry.value ? (openBlock(), createElementBlock("section", _hoisted_27, [
            createBaseVNode("div", _hoisted_28, [
              _cache[21] || (_cache[21] = createBaseVNode("div", { class: "flex items-center justify-center w-20 h-20 bg-green-500 rounded-full mx-auto shadow-lg" }, [
                createBaseVNode("svg", {
                  class: "w-12 h-12 text-white",
                  fill: "none",
                  stroke: "currentColor",
                  viewBox: "0 0 24 24"
                }, [
                  createBaseVNode("path", {
                    "stroke-linecap": "round",
                    "stroke-linejoin": "round",
                    "stroke-width": "3",
                    d: "M5 13l4 4L19 7"
                  })
                ])
              ], -1)),
              _cache[22] || (_cache[22] = createBaseVNode("h2", { class: "text-3xl font-bold text-green-800" }, "🎉 Payment Successful!", -1)),
              createBaseVNode("div", _hoisted_29, [
                _cache[17] || (_cache[17] = createBaseVNode("p", { class: "text-lg font-semibold text-gray-700" }, "Amount Received", -1)),
                createBaseVNode("p", _hoisted_30, "NPR " + toDisplayString(formatAmount(paymentAmount.value)), 1)
              ]),
              createBaseVNode("p", _hoisted_31, [
                _cache[18] || (_cache[18] = createTextVNode("Customer: ")),
                createBaseVNode("span", _hoisted_32, toDisplayString((_a = selectedCustomer.value) == null ? void 0 : _a.customer_name), 1)
              ]),
              paymentEntry.value ? (openBlock(), createElementBlock("p", _hoisted_33, [
                _cache[19] || (_cache[19] = createTextVNode(" Payment Entry: ")),
                createBaseVNode("a", {
                  href: `/app/payment-entry/${paymentEntry.value}`,
                  class: "text-blue-600 hover:text-blue-800 underline font-semibold",
                  target: "_blank",
                  rel: "noopener"
                }, toDisplayString(paymentEntry.value), 9, _hoisted_34)
              ])) : createCommentVNode("", true),
              createBaseVNode("button", {
                onClick: resetForNextPayment,
                class: "inline-flex items-center px-8 py-4 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 transition-all duration-200 shadow-lg hover:shadow-xl"
              }, _cache[20] || (_cache[20] = [
                createBaseVNode("svg", {
                  class: "w-5 h-5 mr-2",
                  fill: "none",
                  stroke: "currentColor",
                  viewBox: "0 0 24 24"
                }, [
                  createBaseVNode("path", {
                    "stroke-linecap": "round",
                    "stroke-linejoin": "round",
                    "stroke-width": "2",
                    d: "M12 4v16m8-8H4"
                  })
                ], -1),
                createTextVNode(" Make New Payment ")
              ]))
            ])
          ])) : createCommentVNode("", true),
          qrData.value ? (openBlock(), createElementBlock("section", _hoisted_35, [
            createBaseVNode("div", _hoisted_36, [
              _cache[32] || (_cache[32] = createBaseVNode("div", { class: "flex-1 text-center" }, [
                createBaseVNode("h3", { class: "text-xl font-semibold text-gray-900 mb-6" }, "QR Code"),
                createBaseVNode("div", {
                  id: "qr-code",
                  class: "flex justify-center"
                })
              ], -1)),
              createBaseVNode("div", _hoisted_37, [
                createBaseVNode("div", _hoisted_38, [
                  createBaseVNode("div", _hoisted_39, [
                    _cache[23] || (_cache[23] = createBaseVNode("div", { class: "text-xs text-gray-500 uppercase tracking-wide mb-2" }, "Payment Status", -1)),
                    createBaseVNode("div", {
                      class: normalizeClass(["text-2xl font-bold", statusColorClass.value])
                    }, toDisplayString(qrStatus.value || "CREATED"), 3)
                  ]),
                  createBaseVNode("div", _hoisted_40, [
                    createBaseVNode("div", _hoisted_41, [
                      _cache[24] || (_cache[24] = createBaseVNode("span", { class: "text-gray-600" }, "Amount:", -1)),
                      createBaseVNode("span", _hoisted_42, "NPR " + toDisplayString(formatAmount(paymentAmount.value)), 1)
                    ]),
                    createBaseVNode("div", _hoisted_43, [
                      _cache[25] || (_cache[25] = createBaseVNode("span", { class: "text-gray-600" }, "Customer:", -1)),
                      createBaseVNode("span", _hoisted_44, toDisplayString((_b = selectedCustomer.value) == null ? void 0 : _b.customer_name), 1)
                    ]),
                    paymentEntry.value ? (openBlock(), createElementBlock("div", _hoisted_45, [
                      _cache[26] || (_cache[26] = createBaseVNode("span", { class: "text-gray-600" }, "Payment Entry:", -1)),
                      createBaseVNode("a", {
                        href: `/app/payment-entry/${paymentEntry.value}`,
                        class: "text-blue-600 hover:text-blue-700 underline font-semibold",
                        target: "_blank",
                        rel: "noopener"
                      }, toDisplayString(paymentEntry.value), 9, _hoisted_46)
                    ])) : createCommentVNode("", true)
                  ])
                ]),
                paymentMessage.value && (qrStatus.value === "PENDING" || qrStatus.value === "SCANNED" || qrStatus.value === "ERROR" || qrStatus.value === "FAILED") ? (openBlock(), createElementBlock("div", {
                  key: 0,
                  class: normalizeClass(["p-4 rounded-lg border", {
                    "bg-orange-50 border-orange-200": qrStatus.value === "PENDING",
                    "bg-yellow-50 border-yellow-200": qrStatus.value === "SCANNED",
                    "bg-red-50 border-red-200": qrStatus.value === "ERROR" || qrStatus.value === "FAILED"
                  }])
                }, [
                  createBaseVNode("div", _hoisted_47, [
                    qrStatus.value === "PENDING" ? (openBlock(), createElementBlock("svg", _hoisted_48, _cache[27] || (_cache[27] = [
                      createBaseVNode("path", {
                        "stroke-linecap": "round",
                        "stroke-linejoin": "round",
                        "stroke-width": "2",
                        d: "M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                      }, null, -1)
                    ]))) : qrStatus.value === "SCANNED" ? (openBlock(), createElementBlock("svg", _hoisted_49, _cache[28] || (_cache[28] = [
                      createBaseVNode("path", {
                        "stroke-linecap": "round",
                        "stroke-linejoin": "round",
                        "stroke-width": "2",
                        d: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                      }, null, -1)
                    ]))) : (openBlock(), createElementBlock("svg", _hoisted_50, _cache[29] || (_cache[29] = [
                      createBaseVNode("path", {
                        "stroke-linecap": "round",
                        "stroke-linejoin": "round",
                        "stroke-width": "2",
                        d: "M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                      }, null, -1)
                    ]))),
                    createBaseVNode("div", _hoisted_51, [
                      createBaseVNode("p", {
                        class: normalizeClass(["text-sm font-medium", {
                          "text-orange-800": qrStatus.value === "PENDING",
                          "text-yellow-800": qrStatus.value === "SCANNED",
                          "text-red-800": qrStatus.value === "ERROR" || qrStatus.value === "FAILED"
                        }])
                      }, toDisplayString(paymentMessage.value), 3)
                    ])
                  ])
                ], 2)) : createCommentVNode("", true),
                createBaseVNode("div", _hoisted_52, [
                  createBaseVNode("button", {
                    onClick: manuallyProcessPayment,
                    class: "flex-1 inline-flex items-center justify-center px-4 py-2 border border-green-300 rounded-md shadow-sm text-sm font-medium text-green-700 bg-white hover:bg-green-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500",
                    disabled: !currentTxName.value || qrStatus.value === "SUCCESS"
                  }, _cache[30] || (_cache[30] = [
                    createBaseVNode("svg", {
                      class: "w-4 h-4 mr-2",
                      fill: "none",
                      stroke: "currentColor",
                      viewBox: "0 0 24 24"
                    }, [
                      createBaseVNode("path", {
                        "stroke-linecap": "round",
                        "stroke-linejoin": "round",
                        "stroke-width": "2",
                        d: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                      })
                    ], -1),
                    createTextVNode(" Process Payment ")
                  ]), 8, _hoisted_53),
                  createBaseVNode("button", {
                    onClick: regenerateQR,
                    class: "flex-1 inline-flex items-center justify-center px-4 py-2 border border-red-300 rounded-md shadow-sm text-sm font-medium text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  }, _cache[31] || (_cache[31] = [
                    createBaseVNode("svg", {
                      class: "w-4 h-4 mr-2",
                      fill: "none",
                      stroke: "currentColor",
                      viewBox: "0 0 24 24"
                    }, [
                      createBaseVNode("path", {
                        "stroke-linecap": "round",
                        "stroke-linejoin": "round",
                        "stroke-width": "2",
                        d: "M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                      })
                    ], -1),
                    createTextVNode(" Reset ")
                  ]))
                ])
              ])
            ])
          ])) : createCommentVNode("", true),
          statusLogs.value.length ? (openBlock(), createElementBlock("section", _hoisted_54, [
            _cache[33] || (_cache[33] = createBaseVNode("h3", { class: "text-lg font-semibold text-gray-900 mb-4" }, "Live Status Updates", -1)),
            createBaseVNode("ul", _hoisted_55, [
              (openBlock(true), createElementBlock(Fragment, null, renderList(statusLogs.value, (log) => {
                return openBlock(), createElementBlock("li", {
                  key: log.id,
                  class: "border border-gray-200 rounded-lg px-4 py-3 bg-gray-50"
                }, [
                  createBaseVNode("div", _hoisted_56, [
                    createBaseVNode("span", {
                      class: normalizeClass([log.levelClass, "text-sm font-medium"])
                    }, toDisplayString(log.levelLabel), 3),
                    createBaseVNode("span", _hoisted_57, toDisplayString(formatLogTime(log.ts)), 1)
                  ]),
                  createBaseVNode("p", _hoisted_58, toDisplayString(log.message), 1)
                ]);
              }), 128))
            ])
          ])) : createCommentVNode("", true),
          showSuccessDialog.value ? (openBlock(), createElementBlock("div", _hoisted_59, [
            createBaseVNode("div", _hoisted_60, [
              createBaseVNode("div", {
                class: "fixed inset-0 bg-gray-900 bg-opacity-75 backdrop-blur-sm transition-opacity",
                "aria-hidden": "true",
                onClick: _cache[4] || (_cache[4] = ($event) => showSuccessDialog.value = false)
              }),
              _cache[40] || (_cache[40] = createBaseVNode("span", {
                class: "hidden sm:inline-block sm:align-middle sm:h-screen",
                "aria-hidden": "true"
              }, "​", -1)),
              createBaseVNode("div", _hoisted_61, [
                _cache[39] || (_cache[39] = createBaseVNode("div", { class: "bg-gradient-to-br from-green-400 to-emerald-500 px-6 pt-8 pb-6" }, [
                  createBaseVNode("div", { class: "mx-auto flex items-center justify-center h-24 w-24 rounded-full bg-white shadow-lg animate-bounce-slow" }, [
                    createBaseVNode("svg", {
                      class: "h-16 w-16 text-green-500",
                      fill: "none",
                      stroke: "currentColor",
                      viewBox: "0 0 24 24"
                    }, [
                      createBaseVNode("path", {
                        "stroke-linecap": "round",
                        "stroke-linejoin": "round",
                        "stroke-width": "3",
                        d: "M5 13l4 4L19 7"
                      })
                    ])
                  ])
                ], -1)),
                createBaseVNode("div", _hoisted_62, [
                  createBaseVNode("div", _hoisted_63, [
                    _cache[37] || (_cache[37] = createBaseVNode("h3", {
                      class: "text-3xl leading-6 font-bold text-gray-900 mb-3",
                      id: "modal-title"
                    }, " 🎉 Payment Successful! ", -1)),
                    createBaseVNode("div", _hoisted_64, [
                      createBaseVNode("div", _hoisted_65, [
                        _cache[34] || (_cache[34] = createBaseVNode("p", { class: "text-sm font-medium text-gray-600 mb-2" }, "Amount Received", -1)),
                        createBaseVNode("p", _hoisted_66, " NPR " + toDisplayString(formatAmount(paymentAmount.value)), 1)
                      ])
                    ]),
                    createBaseVNode("div", _hoisted_67, [
                      createBaseVNode("p", _hoisted_68, [
                        _cache[35] || (_cache[35] = createBaseVNode("span", { class: "font-semibold" }, "Customer:", -1)),
                        createTextVNode(" " + toDisplayString((_c = selectedCustomer.value) == null ? void 0 : _c.customer_name), 1)
                      ]),
                      paymentEntry.value ? (openBlock(), createElementBlock("p", _hoisted_69, [
                        _cache[36] || (_cache[36] = createBaseVNode("span", { class: "font-semibold" }, "Payment Entry:", -1)),
                        createBaseVNode("a", {
                          href: `/app/payment-entry/${paymentEntry.value}`,
                          class: "text-blue-600 hover:text-blue-800 underline font-semibold",
                          target: "_blank",
                          rel: "noopener"
                        }, toDisplayString(paymentEntry.value), 9, _hoisted_70)
                      ])) : createCommentVNode("", true),
                      createBaseVNode("p", _hoisted_71, toDisplayString((/* @__PURE__ */ new Date()).toLocaleString()), 1)
                    ])
                  ])
                ]),
                createBaseVNode("div", _hoisted_72, [
                  createBaseVNode("button", {
                    type: "button",
                    onClick: resetForNextPayment,
                    class: "w-full inline-flex justify-center items-center rounded-lg border border-transparent shadow-sm px-6 py-3 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:w-auto transition-all duration-200"
                  }, _cache[38] || (_cache[38] = [
                    createBaseVNode("svg", {
                      class: "w-5 h-5 mr-2",
                      fill: "none",
                      stroke: "currentColor",
                      viewBox: "0 0 24 24"
                    }, [
                      createBaseVNode("path", {
                        "stroke-linecap": "round",
                        "stroke-linejoin": "round",
                        "stroke-width": "2",
                        d: "M12 4v16m8-8H4"
                      })
                    ], -1),
                    createTextVNode(" Make New Payment ")
                  ])),
                  createBaseVNode("button", {
                    type: "button",
                    onClick: _cache[5] || (_cache[5] = ($event) => showSuccessDialog.value = false),
                    class: "mt-3 w-full inline-flex justify-center rounded-lg border border-gray-300 shadow-sm px-6 py-3 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:w-auto transition-all duration-200"
                  }, " OK ")
                ])
              ])
            ])
          ])) : createCommentVNode("", true),
          showErrorDialog.value ? (openBlock(), createElementBlock("section", _hoisted_73, [
            createBaseVNode("div", _hoisted_74, [
              _cache[41] || (_cache[41] = createBaseVNode("div", { class: "flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mx-auto" }, [
                createBaseVNode("svg", {
                  class: "w-8 h-8 text-red-600",
                  fill: "none",
                  stroke: "currentColor",
                  viewBox: "0 0 24 24"
                }, [
                  createBaseVNode("path", {
                    "stroke-linecap": "round",
                    "stroke-linejoin": "round",
                    "stroke-width": "2",
                    d: "M6 18L18 6M6 6l12 12"
                  })
                ])
              ], -1)),
              _cache[42] || (_cache[42] = createBaseVNode("h3", { class: "text-2xl font-bold text-gray-900" }, "Payment Failed", -1)),
              createBaseVNode("p", _hoisted_75, toDisplayString(paymentMessage.value), 1),
              createBaseVNode("div", { class: "flex gap-3 justify-center" }, [
                createBaseVNode("button", {
                  onClick: regenerateQRFromDialog,
                  class: "inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
                }, " Regenerate QR "),
                createBaseVNode("button", {
                  onClick: resetAll,
                  class: "inline-flex items-center px-6 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors duration-200"
                }, " Reset All ")
              ])
            ])
          ])) : createCommentVNode("", true)
        ]),
        showLoadingOverlay.value ? (openBlock(), createBlock(LoadingOverlay, { key: 0 })) : createCommentVNode("", true)
      ]);
    };
  }
};
const QRPay = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-1308ca85"]]);
export {
  QRPay as default
};
//# sourceMappingURL=QRPay-DlEhN-6t.js.map
