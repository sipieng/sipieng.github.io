document.addEventListener('DOMContentLoaded', async function() {
    // Add mobile menu functionality
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const navOverlay = document.getElementById('nav-overlay');
    const aside = document.querySelector('aside');

    function toggleMobileMenu() {
        aside.classList.toggle('nav-open');
        navOverlay.classList.toggle('open');
        // Toggle menu button icon
        const icon = mobileMenuButton.querySelector('i');
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
    }

    mobileMenuButton.addEventListener('click', toggleMobileMenu);
    navOverlay.addEventListener('click', toggleMobileMenu);

    // Close mobile menu when clicking a nav link
    document.addEventListener('click', function(event) {
        if (event.target.closest('.nav-link') && window.innerWidth < 1024) {
            toggleMobileMenu();
        }
    });

    try {
        const response = await fetch('config.json');
        if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
        const config = await response.json();

        // Update title
        document.title = config.title;
        document.querySelector('h1').textContent = config.title;

        // Update cover image
        document.querySelector('img').src = config.coverImage;

        // Update navigation
        const navList = document.querySelector('nav ul');
        navList.innerHTML = '';
        config.episodes.forEach((episode, index) => {
            const li = document.createElement('li');
            li.innerHTML = `<a href="#" class="nav-link flex items-center py-2 px-3 rounded text-gray-700 hover:bg-gray-200 hover:scale-105 transition-transform duration-150 ease-in-out" data-episode="${index + 1}">
                            <i class="fas fa-file-lines w-5 mr-2 text-blue-600"></i> ${episode.title}
                        </a>`;
            navList.appendChild(li);
        });

        // Update content area with episode divs
        const contentArea = document.getElementById('content-area');
        contentArea.innerHTML = '';
        config.episodes.forEach((episode, index) => {
            const div = document.createElement('div');
            div.id = `episode-${index + 1}`;
            div.className = 'episode-content prose max-w-none prose-indigo lg:prose-lg';
            contentArea.appendChild(div);
        });

        // Re-attach event listeners for new nav links
        const navLinks = document.querySelectorAll('.nav-link');
        const contentSections = document.querySelectorAll('.episode-content');
        const bottomNav = document.getElementById('episode-navigation');
        const prevLink = document.getElementById('prev-episode-link');
        const nextLink = document.getElementById('next-episode-link');
        const prevLinkText = prevLink.querySelector('.link-text');
        const nextLinkText = nextLink.querySelector('.link-text');

        // --- Function to Update Bottom Navigation ---
        function updateBottomNavigation(currentEpisode) {
            const episodeNum = parseInt(currentEpisode, 10);
            const totalEpisodes = config.episodes.length;

            // Reset links
            prevLink.style.display = 'none';
            nextLink.style.display = 'none';
            prevLink.setAttribute('data-target-episode', '');
            nextLink.setAttribute('data-target-episode', '');

            // Show/Update Previous Link
            if (episodeNum > 1) {
                const prevEpisodeNum = episodeNum - 1;
                prevLinkText.textContent = config.episodes[prevEpisodeNum - 1].title;
                prevLink.setAttribute('data-target-episode', prevEpisodeNum);
                prevLink.style.display = 'inline-flex';
            }

            // Show/Update Next Link
            if (episodeNum < totalEpisodes) {
                const nextEpisodeNum = episodeNum + 1;
                nextLinkText.textContent = config.episodes[nextEpisodeNum - 1].title;
                nextLink.setAttribute('data-target-episode', nextEpisodeNum);
                nextLink.style.display = 'inline-flex';
            }
        }

        // --- Function to Load and Render Markdown ---
        async function loadEpisode(episodeNumber) {
            const targetSection = document.getElementById(`episode-${episodeNumber}`);
            if (!targetSection) return; // Exit if target div doesn't exist

            // Hide all other content sections first
            contentSections.forEach(section => {
                if (section.id !== `episode-${episodeNumber}`) {
                    section.style.display = 'none';
                    section.innerHTML = ''; // Clear content of hidden sections
                }
            });

            // Show loading message
            targetSection.innerHTML = '<p class="loading-message">Loading content...</p>';
            targetSection.style.display = 'block';

            const filename = `${config.episodes[episodeNumber - 1].id}.${config.fileExtension}`;

            try {
                const response = await fetch(filename);
                if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
                const markdownText = await response.text();

                if (typeof marked === 'undefined' || typeof marked.parse !== 'function') {
                    console.error("Marked.js library is not loaded correctly.");
                    targetSection.innerHTML = '<p class="error-message">Error: Markdown library not loaded.</p>';
                    return;
                }
                targetSection.innerHTML = marked.parse(markdownText, { breaks: true });

                // *** UPDATE BOTTOM NAVIGATION after content loaded ***
                updateBottomNavigation(episodeNumber);

            } catch (error) {
                console.error('Error loading or rendering episode:', error);
                targetSection.innerHTML = `<p class="error-message">Error loading content for ${config.episodes[episodeNumber - 1].title}. Please check if '${filename}' exists and the server is configured correctly.</p>`;
                updateBottomNavigation(0);
            }
        }

        // --- Event Listener for Sidebar Navigation Links ---
        navLinks.forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();
                const targetEpisode = this.getAttribute('data-episode');

                // Update active link style in sidebar
                navLinks.forEach(nav => nav.classList.remove('active'));
                this.classList.add('active');

                // Load the selected episode content
                loadEpisode(targetEpisode);

                // Scroll to top of content area
                if (window.innerWidth < 1024) {
                    // For mobile, wait for menu to close before scrolling
                    setTimeout(() => {
                        window.scrollTo({
                            top: 0,
                            behavior: 'smooth'
                        });
                    }, 300); // Match the transition duration
                } else {
                    // For desktop, scroll immediately
                    contentArea.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });

        // --- Event Listener for Bottom Navigation Links ---
        bottomNav.addEventListener('click', function(event) {
            const targetLink = event.target.closest('a'); // Find nearest parent <a>
            // Check if a valid prev/next link was clicked
            if (targetLink && (targetLink.id === 'prev-episode-link' || targetLink.id === 'next-episode-link')) {
                event.preventDefault();
                const targetEpisode = targetLink.getAttribute('data-target-episode');
                if (targetEpisode) {
                    // Find the corresponding sidebar link and update its state
                    const sidebarLink = document.querySelector(`.nav-link[data-episode="${targetEpisode}"]`);
                    if (sidebarLink) {
                        // Update active state without triggering click
                        navLinks.forEach(nav => nav.classList.remove('active'));
                        sidebarLink.classList.add('active');
                        
                        // Load content directly
                        loadEpisode(targetEpisode);
                        
                        // Scroll to top
                        window.scrollTo({
                            top: 0,
                            behavior: 'smooth'
                        });
                    }
                }
            }
        });

        // Initial load of the first episode
        loadEpisode('1');
        const initialActiveLink = document.querySelector('.nav-link[data-episode="1"]');
        if (initialActiveLink) {
            navLinks.forEach(nav => nav.classList.remove('active'));
            initialActiveLink.classList.add('active');
        }

    } catch (error) {
        console.error('Error loading config:', error);
    }
}); 