from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProductProgram
from .forms import ProductProgramForm

@login_required
def program_list(request):
    if request.method == 'POST':
        program_id = request.POST.get('program_id')
        if program_id:
            program = get_object_or_404(ProductProgram, id=program_id)
            form = ProductProgramForm(request.POST, instance=program)
        else:
            form = ProductProgramForm(request.POST)

        if form.is_valid():
            program = form.save(commit=False)
            program.created_by = request.user
            program.save()
            return redirect('program_list')
    else:
        form = ProductProgramForm()

    programs = ProductProgram.objects.select_related('created_by').order_by('-created_at')
    return render(request, 'product_program/program_list.html', {
        'form': form,
        'programs': programs
    })

@login_required
def delete_program(request, pk):
    program = get_object_or_404(ProductProgram, pk=pk)
    if request.method == "POST":
        program.delete()
    return redirect('program_list')
