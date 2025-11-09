from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from .models import ShortLink
from .forms import ShortLinkForm


def redirect_view(request, path):
    """
    Handle /go/<path> redirects.
    Supports simple jumps, parameter forwarding, and prefix matching.
    Priority: exact matches (simple/forward) > prefix matches (prefix/prefix-forward)
    """
    # First, try exact match with simple or forward mode
    try:
        short_link = ShortLink.objects.get(
            slug=path, 
            is_active=True,
            jump_type__in=['simple', 'forward']
        )
        extra_path = ''
    except ShortLink.DoesNotExist:
        # If no exact match, try prefix matching
        short_link = None
        extra_path = ''
        
        # Look for prefix matches - find all prefix-type links that could match
        prefix_links = ShortLink.objects.filter(
            is_active=True,
            jump_type__in=['prefix', 'prefix-forward'],
            slug__endswith='/'
        ).order_by('-slug')  # Order by slug descending to match longest prefix first
        
        for candidate in prefix_links:
            # Check if the path starts with this prefix
            if path.startswith(candidate.slug):
                short_link = candidate
                # Extract the extra path after the prefix
                extra_path = path[len(candidate.slug):]
                break
        
        if not short_link:
            raise Http404("Short link not found")
    
    # Increment click counter
    short_link.increment_clicks()
    
    # Get the destination URL
    destination = short_link.destination_url
    
    # Handle prefix modes: append extra path
    if short_link.jump_type in ['prefix', 'prefix-forward'] and extra_path:
        # Ensure destination ends with / if extra_path doesn't start with /
        if not destination.endswith('/') and not extra_path.startswith('/'):
            destination = destination + '/'
        destination = destination + extra_path
    
    # If jump type is 'forward' or 'prefix-forward', append query parameters
    if short_link.jump_type in ['forward', 'prefix-forward'] and request.GET:
        # Parse the destination URL
        parsed_url = urlparse(destination)
        
        # Get existing query parameters from destination
        existing_params = parse_qs(parsed_url.query)
        
        # Merge with incoming parameters (incoming params take precedence)
        merged_params = {**existing_params}
        for key, value in request.GET.items():
            merged_params[key] = [value]
        
        # Build new query string
        # Flatten the list values (take first value for each key)
        flat_params = {k: v[0] if isinstance(v, list) else v for k, v in merged_params.items()}
        new_query = urlencode(flat_params)
        
        # Reconstruct URL with new query string
        destination = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment
        ))
    
    # Redirect with 302 (temporary redirect)
    return redirect(destination)


@login_required
def portal_home(request):
    """
    Main portal page showing all short links.
    """
    search_query = request.GET.get('search', '')
    
    links = ShortLink.objects.all()
    
    if search_query:
        links = links.filter(
            Q(slug__icontains=search_query) |
            Q(destination_url__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'links': links,
        'search_query': search_query,
        'total_clicks': sum(link.click_count for link in ShortLink.objects.all()),
        'total_links': ShortLink.objects.count(),
        'active_links': ShortLink.objects.filter(is_active=True).count(),
    }
    
    return render(request, 'shortener/portal_home.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def link_create(request):
    """Create a new short link."""
    if request.method == 'POST':
        form = ShortLinkForm(request.POST)
        if form.is_valid():
            link = form.save()
            messages.success(request, f'Short link created: /go/{link.slug}')
            return redirect('portal_home')
    else:
        form = ShortLinkForm()
    
    return render(request, 'shortener/link_form.html', {
        'form': form,
        'title': 'Create New Short Link'
    })


@login_required
@require_http_methods(["GET", "POST"])
def link_edit(request, pk):
    """Edit an existing short link."""
    link = get_object_or_404(ShortLink, pk=pk)
    
    if request.method == 'POST':
        form = ShortLinkForm(request.POST, instance=link)
        if form.is_valid():
            link = form.save()
            messages.success(request, f'Short link updated: /go/{link.slug}')
            return redirect('portal_home')
    else:
        form = ShortLinkForm(instance=link)
    
    return render(request, 'shortener/link_form.html', {
        'form': form,
        'title': f'Edit Short Link: /go/{link.slug}',
        'link': link
    })


@login_required
@require_http_methods(["POST"])
def link_delete(request, pk):
    """Delete a short link."""
    link = get_object_or_404(ShortLink, pk=pk)
    slug = link.slug
    link.delete()
    messages.success(request, f'Short link deleted: /go/{slug}')
    return redirect('portal_home')


@login_required
@require_http_methods(["POST"])
def link_toggle_active(request, pk):
    """Toggle the active status of a link."""
    link = get_object_or_404(ShortLink, pk=pk)
    link.is_active = not link.is_active
    link.save()
    
    status = "activated" if link.is_active else "deactivated"
    messages.success(request, f'Short link {status}: /go/{link.slug}')
    return redirect('portal_home')
