<script setup>
    import { onSlideEnter, onSlideLeave, useDarkMode, useIsSlideActive, useNav, useSlideContext } from '@slidev/client'
    const { $slidev } = useSlideContext()
    const { isDark } = useDarkMode()
    const { currentPage, currentLayout, currentSlideRoute } = useNav()

</script>
