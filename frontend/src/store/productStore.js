import create from 'zustand';
import api from './api';

const useProductStore = create((set) => ({
    products: [],
    currentProduct: null,
    isLoading: false,
    error: null,

    fetchProducts: async () => {
        set({ isLoading: true, error: null });
        try {
            const response = await api.get('/products');
            set({ products: response.data.products, isLoading: false });
        } catch (error) {
            set({ error: error.response?.data?.error || 'Failed to fetch products', isLoading: false });
        }
    },

    getProduct: async (id) => {
        try {
            const response = await api.get(`/products/${id}`);
            set({ currentProduct: response.data });
        } catch (error) {
            console.error('Failed to get product', error);
        }
    },

    createProduct: async (productData) => {
        set({ isLoading: true, error: null });
        try {
            const response = await api.post('/products', productData);
            set((state) => ({
                products: [...state.products, response.data.product],
                isLoading: false,
            }));
            return response.data;
        } catch (error) {
            set({ error: error.response?.data?.error || 'Failed to create product', isLoading: false });
        }
    },

    updateProduct: async (id, productData) => {
        set({ isLoading: true, error: null });
        try {
            const response = await api.put(`/products/${id}`, productData);
            set((state) => ({
                products: state.products.map((p) => (p.id === id ? response.data.product : p)),
                isLoading: false,
            }));
            return response.data;
        } catch (error) {
            set({ error: error.response?.data?.error || 'Failed to update product', isLoading: false });
        }
    },

    deleteProduct: async (id) => {
        set({ isLoading: true, error: null });
        try {
            await api.delete(`/products/${id}`);
            set((state) => ({
                products: state.products.filter((p) => p.id !== id),
                isLoading: false,
            }));
        } catch (error) {
            set({ error: error.response?.data?.error || 'Failed to delete product', isLoading: false });
        }
    },
}));

export default useProductStore;
