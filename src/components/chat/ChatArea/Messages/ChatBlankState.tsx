'use client'

import { motion } from 'framer-motion'

const ChatBlankState = () => {
  return (
    <section
      className="flex flex-col items-center justify-center text-center min-h-[400px] px-8"
      aria-label="Mensagem de boas-vindas"
    >
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="flex flex-col items-center gap-8 max-w-2xl"
      >

        {/* Título principal */}
            <motion.h1
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.6 }}
              className="text-heading-1 text-default-font mb-6 text-balance"
            >
              <span className="text-default-font">Gabi<span className="text-brand-blue">.</span></span>
            </motion.h1>

        {/* Subtítulo */}
            <motion.p
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.8 }}
              className="text-body text-subtext-color font-normal leading-relaxed text-balance max-w-2xl"
            >
              Chat Multi-Agentes com tecnologia avançada.
              <br />
              Comece uma conversa digitando sua mensagem abaixo.
            </motion.p>

        {/* Powered by ness. */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 1.0 }}
              className="text-caption text-subtext-color font-light"
            >
              powered by <span className="text-default-font">ness<span className="text-brand-blue">.</span></span>
            </motion.div>
      </motion.div>
    </section>
  )
}

export default ChatBlankState
