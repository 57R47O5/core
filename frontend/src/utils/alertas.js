import toastr from "toastr";
import "toastr/build/toastr.min.css";
import "../utils/custom-toastr.css";


export const Tipo = {
  ERROR: "error",
  WARNING: "warning",
  INFO: "info",
  SUCCESS: "success"
};

export const Alertar = (msg, tipo, titulo) => {
  toastr.options = {
    closeButton: true,
    debug: false,
    newestOnTop: true,
    progressBar: true,
    positionClass: "toast-top-center",
    preventDuplicates: false,
    onclick: null,
    showDuration: "1000",
    hideDuration: "1000",
    timeOut: "4000",
    extendedTimeOut: "5000",
    showEasing: "swing",
    hideEasing: "linear",
    showMethod: "fadeIn",
    hideMethod: "fadeOut",
    containerId: 'toast-container'
  };

  switch (tipo) {
    case Tipo.ERROR:
      toastr.error(msg, titulo);
      break;

    case Tipo.WARNING:
      toastr.warning(msg, titulo);
      break;

    case Tipo.INFO:
      toastr.info(msg, titulo);
      break;

    case Tipo.SUCCESS:
      toastr.success(msg, titulo);
      break;

    default:
      toastr.success(msg, titulo);
      break;
  }
};

export function alertarExito(response, mensajeDefault) {
  const mensaje = response?.mensaje || mensajeDefault;
  Alertar(mensaje, Tipo.SUCCESS, "Éxito");
}