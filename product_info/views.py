# product_info/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm
from product_program.models import ProductProgram

# 1. 프로그램 선택 화면
@login_required
def select_program(request):
    programs = ProductProgram.objects.filter(is_deleted=False, is_active=True)
    return render(request, 'product_info/select_program.html', {'programs': programs})

# 2. 선택된 프로그램의 제품 목록
@login_required
def product_list(request, program_id):
    program = get_object_or_404(ProductProgram, pk=program_id)
    products = Product.objects.filter(program=program, is_deleted=False)
    return render(request, 'product_info/product_list.html', {
        'program': program,
        'program_id': program.id,
        'products': products
    })

# 3. 신규 등록
@login_required
def product_create(request, program_id):
    program = get_object_or_404(ProductProgram, pk=program_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.program = program
            product.created_by = request.user
            product.updated_by = request.user
            product.save()
            return redirect('product_list', program_id=program_id)
    else:
        form = ProductForm(initial={'program': program})
    return render(request, 'product_info/product_form.html', {
        'form': form,
        'program': program
    })

# 4. 상세 및 수정
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_deleted=False)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.updated_by = request.user
            product.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_info/product_detail.html', {
        'form': form,
        'product': product
    })

# 5. 삭제 (소프트 딜리트)
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, is_deleted=False)
    program_id = product.program.id
    product.is_deleted = True
    product.save()
    return redirect('product_list', program_id=program_id)


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            updated_product = form.save(commit=False)
            updated_product.updated_by = request.user
            updated_product.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_info/product_form.html', {
        'form': form,
        'is_update': True,
        'product': product
    })
