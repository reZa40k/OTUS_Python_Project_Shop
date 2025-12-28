from celery import shared_task


@shared_task
def info_add_poduct(product_name: str) -> str:
    """
    Выводит информацию о добавлении товара в консоль
    """
    msg = f"Добавлен новый товар: {product_name}"
    print(msg)
    return msg


@shared_task
def info_edit_poduct(product_name: str) -> str:
    """
    Выводит информацию об изменении товара в консоль
    """
    msg = f"Изменен товар: {product_name}"
    print(msg)
    return msg


@shared_task
def info_del_poduct(product_name: str) -> str:
    """
    Выводит информацию об удаленном товаре в консоль
    """
    msg = f"Удален товар: {product_name}"
    print(msg)
    return msg
