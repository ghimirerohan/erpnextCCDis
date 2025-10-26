import { d as defineComponent, a as createElementBlock, z as createVNode, A as withCtx, aa as resolveComponent, o as openBlock, b as createBaseVNode, L as unref, I as createTextVNode, N as withModifiers } from "./vendor-DNPaXrxF.js";
import { s as session } from "./index-GzXbegLD.js";
import "./ui-C-4uyU25.js";
const _hoisted_1 = { class: "m-3 flex flex-row items-center justify-center" };
const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "Login",
  setup(__props) {
    function submit(e) {
      const formData = new FormData(e.target);
      session.login.submit({
        email: formData.get("email"),
        password: formData.get("password")
      });
    }
    return (_ctx, _cache) => {
      const _component_Input = resolveComponent("Input");
      const _component_Button = resolveComponent("Button");
      const _component_Card = resolveComponent("Card");
      return openBlock(), createElementBlock("div", _hoisted_1, [
        createVNode(_component_Card, {
          title: "Login to your FrappeUI App!",
          class: "w-full max-w-md mt-4"
        }, {
          default: withCtx(() => [
            createBaseVNode("form", {
              class: "flex flex-col space-y-2 w-full",
              onSubmit: withModifiers(submit, ["prevent"])
            }, [
              createVNode(_component_Input, {
                required: "",
                name: "email",
                type: "text",
                placeholder: "johndoe@email.com",
                label: "User ID"
              }),
              createVNode(_component_Input, {
                required: "",
                name: "password",
                type: "password",
                placeholder: "••••••",
                label: "Password"
              }),
              createVNode(_component_Button, {
                loading: unref(session).login.loading,
                variant: "solid"
              }, {
                default: withCtx(() => _cache[0] || (_cache[0] = [
                  createTextVNode("Login")
                ])),
                _: 1,
                __: [0]
              }, 8, ["loading"])
            ], 32)
          ]),
          _: 1
        })
      ]);
    };
  }
});
export {
  _sfc_main as default
};
//# sourceMappingURL=Login-D07x9gp5.js.map
