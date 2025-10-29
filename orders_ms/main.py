"""
FastAPI Application - Orders Microservice
Mi primer endpoint para entender FastAPI
"""
import uvicorn
import logging
from fastapi import FastAPI, HTTPException, status
from config.logging_config import setup_dev_logging
from fastapi.middleware.cors import CORSMiddleware
from container import Container
from application.dtos.create_order_dtos import CreateOrderRequestDTO
from application.dtos.add_item_to_order_dtos import AddItemToOrderRequestDTO
from application.dtos.get_order_dtos import GetOrderRequestDTO
from application.dtos.list_orders_dtos import ListOrdersRequestDTO
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Inicializar sistema de logging
setup_dev_logging()

# Crear la aplicación FastAPI
app = FastAPI()

# Configurar CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Endpoint para servir la página principal
@app.get("/app")
async def serve_frontend():
    return FileResponse("static/index.html")

# Definir un endpoint simple
@app.get("/favicon.ico")
def favicon():
    return {"message": "No favicon"}

# Modelos para HTTP requests (diferentes a los DTOs de aplicación)
class CreateOrderRequest(BaseModel):
    customer_id: str

class AddItemRequest(BaseModel):
    sku: str
    quantity: int

# Crear el Container (Dependency Injection)
container = Container()
app.container = container # Adjuntar para acceso en tests

# Endpoint para crear órdenes
@app.post("/orders")
def create_order(request: CreateOrderRequest):
    # 1. Convertir HTTP request a DTO de aplicación
    dto = CreateOrderRequestDTO(customer_id=request.customer_id)
    
    # 2. Usar el caso de uso
    use_case = container.create_order_use_case()
    response_dto = use_case.execute(dto)
    
    # 3. Devolver respuesta HTTP
    return {
        "order_id": response_dto.order_id,
        "message": "Order created successfully"
    }

# Endpoint para añadir items
@app.post("/orders/{order_id}/items")
def add_item_to_order(order_id: str, request: AddItemRequest):
    print(f"🔍 DEBUG: Añadiendo item - Order ID: {order_id}, SKU: {request.sku}, Quantity: {request.quantity}")
    
    try:
        # 1. Convertir HTTP request a DTO de aplicación
        dto = AddItemToOrderRequestDTO(
            order_id=order_id,
            sku=request.sku,
            quantity=request.quantity
        )
        
        # 2. Usar el caso de uso
        use_case = container.add_item_use_case()
        response_dto = use_case.execute(dto)
        
        print(f"🔍 DEBUG: Respuesta del use case - Success: {response_dto.success}")
        
        # 3. Devolver respuesta HTTP
        return {
            "success": response_dto.success,
            "message": "Item added successfully" if response_dto.success else "Failed to add item"
        }
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

# Endpoint para obtener detalles de una orden
@app.get("/orders/{order_id}", status_code=200)
def get_order(order_id: str):
    """
    Obtiene los detalles de una orden específica
    
    Returns:
        200: Orden encontrada exitosamente
        404: Orden no encontrada
        500: Error interno del servidor
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Getting order details for order_id: {order_id}")
    
    try:
        # 1. Convertir a DTO de aplicación
        dto = GetOrderRequestDTO(order_id=order_id)
        
        # 2. Usar el caso de uso (lógica de dominio)
        use_case = container.get_order_use_case()
        response_dto = use_case.execute(dto)
        
        # 3. Validar resultado del dominio
        if not response_dto:
            logger.warning(f"Order not found: {order_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order {order_id} not found"
            )
        
        logger.info(f"Order {order_id} retrieved successfully with {response_dto.items_count} items")
        
        # 4. Devolver respuesta HTTP (capa de presentación)
        return {
            "order_id": response_dto.order_id,
            "customer_id": response_dto.customer_id,
            "items": response_dto.items,
            "total_amount": response_dto.total_amount,
            "items_count": response_dto.items_count
        }
        
    except HTTPException:
        # Re-lanzar HTTPException (mantener códigos específicos)
        raise
    except Exception as e:
        # Error interno: no exponer detalles al cliente
        logger.error(f"Internal error getting order {order_id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

# Endpoint para listar todas las órdenes
@app.get("/orders", status_code=200)
def list_orders():
    """
    Lista todas las órdenes del sistema
    
    Returns:
        200: Lista de órdenes obtenida exitosamente
        500: Error interno del servidor
    """
    logger = logging.getLogger(__name__)
    logger.info("Listing all orders")
    
    try:
        # 1. Crear DTO de petición
        dto = ListOrdersRequestDTO()
        
        # 2. Usar el caso de uso (lógica de dominio)
        use_case = container.list_orders_use_case()
        response_dto = use_case.execute(dto)
        
        logger.info(f"Retrieved {response_dto.total_orders} orders successfully")
        
        # 3. Convertir a respuesta HTTP (capa de presentación)
        orders_data = []
        for order_summary in response_dto.orders:
            orders_data.append({
                "order_id": order_summary.order_id,
                "customer_id": order_summary.customer_id,
                "items_count": order_summary.items_count,
                "total_amount": float(order_summary.total_amount)  # Convertir Decimal a float para JSON
            })
        
        return {
            "orders": orders_data,
            "total_orders": response_dto.total_orders
        }
        
    except Exception as e:
        # Error interno: no exponer detalles al cliente
        logger.error(f"Internal error listing orders: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@app.get("/")
def read_root():
    return {"message": "Orders Microservice - Clean Architecture", "status": "running"}

# Ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, reload_dirs=["."])