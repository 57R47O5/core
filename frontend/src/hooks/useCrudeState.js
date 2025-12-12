import { useState } from "react";

export default function useCrudState(api) {
  const [items, setItems] = useState([]);
  const [item, setItem] = useState(null);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("list"); // list | form-new | form-edit

  const list = async (filters = {}) => {
    setLoading(true);
    try {
      const response = await api.listar(filters);
      setItems(response.data);

      // acceso directo si solo hay un resultado
      if (response.length === 1) {
        setItem(response[0]);
        setMode("form-edit");
      }
    } finally {
      setLoading(false);
    }
  };

  const load = async (id) => {
    setLoading(true);
    try {
      const response = await api.obtener(id);
      setItem(response);
      setMode("form-edit");
    } finally {
      setLoading(false);
    }
  };

  const create = async (data) => {
    setLoading(true);
    try {
      await api.crear(data);
      setMode("list");
      await list();
    } finally {
      setLoading(false);
    }
  };

  const update = async (id, data) => {
    setLoading(true);
    try {
      await api.editar(id, data);
      setMode("list");
      await list();
    } finally {
      setLoading(false);
    }
  };

  const remove = async (id) => {
    setLoading(true);
    try {
      await api.eliminar(id);
      setMode("list");
      await list();
    } finally {
      setLoading(false);
    }
  };

  return {
    items,
    item,
    loading,
    mode,
    list,
    load,
    create,
    update,
    remove,
    setMode,
    setItem,
  };
}
