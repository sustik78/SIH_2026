import React, { useState, useEffect } from 'react';
import { apiGetJson } from '../utils/api';
import { 
  Package, 
  Search, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle, 
  Building2, 
  Scale, 
  Clock, 
  ArrowUpRight
} from 'lucide-react';

export const ProductRepositoryPage = ({ onSelectInspection }) => {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async (searchTerm = '') => {
    try {
      setLoading(true);
      const url = searchTerm ? `/api/products?search=${encodeURIComponent(searchTerm)}` : '/api/products';
      const data = await apiGetJson(url);
      setProducts(data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchProducts(search);
  };

  return (
    <div className="space-y-6 pb-16">
      {/* Header */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-blue-700 uppercase tracking-wider mb-1">
            <Package className="w-4 h-4" />
            <span>Master Catalog & Repeat Infractions</span>
          </div>
          <h1 className="text-2xl font-extrabold text-slate-900 font-['Outfit']">
            Packaged Commodity Repository
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Track historical compliance and manufacturer audit records across all inspected brands.
          </p>
        </div>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-3">
        <div className="flex-1 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search products by brand, commodity name, or manufacturer..."
            className="w-full text-xs pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 font-medium"
          />
        </div>
        <button
          type="submit"
          className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow transition-all shrink-0"
        >
          Search Catalog
        </button>
      </form>

      {/* Product Grid */}
      {loading ? (
        <div className="p-12 text-center text-xs font-semibold text-slate-500">
          Loading product catalog...
        </div>
      ) : products.length === 0 ? (
        <div className="p-12 text-center text-xs text-slate-500 bg-white rounded-2xl border border-slate-200">
          No packaged commodities found in repository.
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((p) => {
            const isCompliant = p.latest_status === 'COMPLIANT';
            const isWarning = p.latest_status === 'PENDING REVIEW';
            return (
              <div key={p.id} className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-5 flex flex-col justify-between space-y-4 hover:shadow-md transition-all">
                <div className="space-y-2">
                  <div className="flex items-start justify-between gap-2">
                    <span className="text-[10px] font-bold text-blue-700 uppercase tracking-wider bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                      {p.category}
                    </span>
                    {p.latest_status && (
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                        isCompliant 
                          ? 'bg-emerald-50 text-emerald-800 border-emerald-300' 
                          : isWarning 
                            ? 'bg-amber-50 text-amber-800 border-amber-300' 
                            : 'bg-rose-50 text-rose-800 border-rose-300'
                      }`}>
                        {p.latest_status}
                      </span>
                    )}
                  </div>

                  <h3 className="text-base font-bold text-slate-900 font-['Outfit']">
                    {p.product_name}
                  </h3>

                  <div className="space-y-1 text-xs text-slate-600">
                    <div className="flex items-center gap-1.5 text-slate-500">
                      <Building2 className="w-3.5 h-3.5 shrink-0" />
                      <span className="truncate">{p.manufacturer_name || 'Manufacturer Unverified'}</span>
                    </div>
                    <div className="flex items-center justify-between pt-1">
                      <span>Declared Net Qty:</span>
                      <span className="font-semibold text-slate-900">{p.declared_net_qty || 'N/A'}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span>Declared MRP:</span>
                      <span className="font-semibold text-slate-900">{p.declared_mrp || 'N/A'}</span>
                    </div>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                  <span className="text-slate-400 text-[11px]">
                    Inspections: <strong className="text-slate-700">{p.inspections_count}</strong>
                  </span>
                  {p.latest_score !== null && (
                    <span className="text-slate-800 font-bold">
                      Latest Score: <span className="text-blue-700">{p.latest_score}/100</span>
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
