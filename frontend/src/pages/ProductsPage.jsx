import React, { useEffect, useState } from 'react';
import useProductStore from '../store/productStore';
import ProductForm from '../components/Products/ProductForm';

const ProductsPage = () => {
    const { products, fetchProducts, deleteProduct, isLoading } = useProductStore();
    const [showForm, setShowForm] = useState(false);
    const [editingProduct, setEditingProduct] = useState(null);

    useEffect(() => {
        fetchProducts();
    }, []);

    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this product?')) {
            await deleteProduct(id);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 p-8">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="flex justify-between items-center mb-8">
                    <div>
                        <h1 className="text-4xl font-bold text-gray-800">🏢 My Products</h1>
                        <p className="text-gray-600 mt-2">Manage your digital products</p>
                    </div>
                    <button
                        onClick={() => {
                            setEditingProduct(null);
                            setShowForm(true);
                        }}
                        className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition"
                    >
                        + Add Product
                    </button>
                </div>

                {/* Form Modal */}
                {showForm && (
                    <ProductForm
                        product={editingProduct}
                        onClose={() => setShowForm(false)}
                        onSuccess={() => {
                            setShowForm(false);
                            fetchProducts();
                        }}
                    />
                )}

                {/* Products Grid */}
                {isLoading ? (
                    <div className="text-center py-12">Loading products...</div>
                ) : products.length === 0 ? (
                    <div className="bg-white rounded-lg shadow-lg p-12 text-center">
                        <p className="text-xl text-gray-600 mb-4">No products yet</p>
                        <button
                            onClick={() => setShowForm(true)}
                            className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                        >
                            Create Your First Product
                        </button>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {products.map((product) => (
                            <div key={product.id} className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition">
                                {product.image_url && (
                                    <img src={product.image_url} alt={product.name} className="w-full h-48 object-cover" />
                                )}
                                <div className="p-6">
                                    <h3 className="text-xl font-bold text-gray-800 mb-2">{product.name}</h3>
                                    <p className="text-gray-600 text-sm mb-3 line-clamp-2">{product.description}</p>
                                    <div className="flex justify-between items-center mb-4">
                                        <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">{product.category}</span>
                                        <span className="text-green-600 font-bold">${product.price?.toFixed(2)}</span>
                                    </div>
                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => {
                                                setEditingProduct(product);
                                                setShowForm(true);
                                            }}
                                            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded transition"
                                        >
                                            Edit
                                        </button>
                                        <button
                                            onClick={() => handleDelete(product.id)}
                                            className="flex-1 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 rounded transition"
                                        >
                                            Delete
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default ProductsPage;
